import click
import click_config_file
import isb_lib.core  # type: ignore
import logging
import datetime
import fileinput
import json

from isamples_sesar.sesar_adapter import SESARItem
from isamples_sesar.sqlmodel_database import SQLModelDAO as SESAR_SQLModelDAO, get_sample_rows
from isamples_sesar.sesar_transformer import Transformer, geo_to_h3
from isb_web.sqlmodel_database import SQLModelDAO as iSB_SQLModelDAO, all_thing_primary_keys, save_or_update_thing, get_thing_with_id, DatabaseBulkUpdater  # type: ignore

BATCH_SIZE = 10000


def load_sesar_entries(sesar_db_session, isb_db_session, start_from=None):
    more_samples = True
    offset = 0
    num_newer = 0
    while (more_samples):
        primary_keys_by_id = all_thing_primary_keys(isb_db_session, SESARItem.AUTHORITY_ID)
        bulk_updater = DatabaseBulkUpdater(
            isb_db_session,
            SESARItem.AUTHORITY_ID,
            BATCH_SIZE,
            SESARItem.MEDIA_TYPE,
            primary_keys_by_id
        )

        samples = get_sample_rows(sesar_db_session, offset, BATCH_SIZE, start_from)
        if (len(samples) == 0):
            more_samples = False
        else:
            for sample in samples:
                current_record = Transformer(sample).transform()
                num_newer += 1
                thing_id = f"igsn:{sample.igsn}"
                resolved_url = f"doi.org/{sample.igsn}"
                h3 = geo_to_h3(sample.latitude, sample.longitude)
                t_created = sample.registration_date
                bulk_updater.add_thing(current_record, thing_id, resolved_url, 200, h3, t_created)
            offset += BATCH_SIZE
            bulk_updater.finish()
    print(f"Num newer={num_newer}\n\n")

def ingest_precalculated_vocab(isb_db_session, json_file):
    count = 0
    with fileinput.FileInput(json_file, inplace = True, backup ='.bak') as file: 
        for line in file:
            if line[:4] == 'done':
                print(line, end='')
                continue
            precalculated_data = json.loads(line)
            if precalculated_data == None:
                continue
            specimen_category = precalculated_data["has_specimen_category"]
            material_category = precalculated_data["has_material_category"]
            context_category = precalculated_data["has_context_category"]
            igsn_suffix = precalculated_data["sample_identifier"][5:]
            if (igsn_suffix[:3] == 'UKB'):
                doi_prefix = '10.60665/'
            elif (igsn_suffix[:3] == 'ODP'):
                doi_prefix = '10.60471/'
            elif (igsn_suffix[:5] == 'IEJAA'):
                doi_prefix = '10.60471/'
            elif (igsn_suffix[:3] == 'NHB'):
                doi_prefix = '10.58151/'
            elif (igsn_suffix[:3] == 'UGS'):
                doi_prefix = '10.58136/'
            elif (igsn_suffix[:3] == 'CNR'):
                doi_prefix = ''
            else:
                doi_prefix = '10.58052/'
            igsn = 'igsn:' + doi_prefix + igsn_suffix
            current_record = get_thing_with_id(isb_db_session, igsn)
            if current_record != None:
                resolved_content_copy = current_record.resolved_content.copy()
                resolved_content_copy["hasSpecimenCategory"] = specimen_category
                resolved_content_copy["hasMaterialCategory"] = material_category
                resolved_content_copy["hasContextCategory"] = context_category
                current_record.resolved_content = resolved_content_copy
                save_or_update_thing(isb_db_session,current_record)
                print('done'+line, end='')
                count+=1
    print('samples updated: ' + str(count))

@click.group()
@click.option(
    "-d", "--sesar_db_url", default=None, help="SQLAlchemy SESAR database URL for retrieving data"
)
@click.option(
    "-d", "--isb_db_url", default=None, help="SQLAlchemy database URL for storage"
)
@click.option("-s", "--solr_url", default=None, help="Solr index URL")
@click.option(
    "-v",
    "--verbosity",
    default="DEBUG",
    help="Specify logging level",
    show_default=True,
)
@click_config_file.configuration_option(config_file_name="sesar.cfg")
@click.pass_context
def main(ctx, sesar_db_url, isb_db_url, solr_url, verbosity):
    isb_lib.core.things_main(ctx, isb_db_url, solr_url, verbosity)
    ctx.obj["sesar_db_url"] = sesar_db_url
    ctx.obj["isb_db_url"] = isb_db_url


@main.command("load")
@click.option(
    "-m",
    "--max_records",
    type=int,
    default=1000,
    help="Maximum records to load, -1 for all",
)
@click.option(
    "-d",
    "--modification_date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=(datetime.datetime.now()-datetime.timedelta(days=1)).date().strftime("%Y-%m-%d"), # default to last day for daily script
    help="""The modified date to use when considering delta updates.  Records with a last modified before this date
    will be ignored"""
)
@click_config_file.configuration_option(config_file_name="sesar.cfg")
@click.pass_context
def load_records(ctx, max_records, modification_date):
    click.echo(modification_date)
    sesar_session = SESAR_SQLModelDAO(ctx.obj["sesar_db_url"]).get_session()
    isb_session = iSB_SQLModelDAO(ctx.obj["isb_db_url"]).get_session()
    logging.info("loadRecords: %s", str(isb_session))
    load_sesar_entries(sesar_session, isb_session, modification_date)
    sesar_session.close()
    isb_session.close()


@main.command("populate_isb_core_solr")
@click.pass_context
def populate_isb_core_solr(ctx):
    logger = isb_lib.core.getLogger()
    db_url = ctx.obj["db_url"]
    solr_url = ctx.obj["solr_url"]
    solr_importer = isb_lib.core.CoreSolrImporter(
        db_url=db_url,
        authority_id=isb_lib.smithsonian_adapter.SESARItem.AUTHORITY_ID,
        db_batch_size=1000,
        solr_batch_size=1000,
        solr_url=solr_url,
    )
    allkeys = solr_importer.run_solr_import(
        isb_lib.smithsonian_adapter.reparse_as_core_record
    )
    logger.info(f"Total keys= {len(allkeys)}")

@main.command("ingest_json")
@click.option(
    "-d",
    "--json_file",
    type=str,
    default="output.json",
    help="""The json file path to be used for ingesting data"""
)
@click_config_file.configuration_option(config_file_name="sesar.cfg")
@click.pass_context
def ingest_json(ctx, json_file):
    click.echo(json_file)
    isb_session = iSB_SQLModelDAO(ctx.obj["isb_db_url"]).get_session()
    ingest_precalculated_vocab(isb_session, json_file)
    isb_session.close()

if __name__ == "__main__":
    main()
