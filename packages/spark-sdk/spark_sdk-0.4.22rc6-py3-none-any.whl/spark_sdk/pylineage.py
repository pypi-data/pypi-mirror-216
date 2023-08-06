import os
import sys
def get_job_id():
    import __main__
    try:
        return __main__.__file__
    except:
        return None
    
def get_flow_id():
    main_module = sys.modules['__main__']
    try:
        return os.path.abspath(main_module.__file__)
    except:
        return None

def extract_project_name(path):
    not_project = ['script', 'dags', 'scripts']
    if os.path.basename(os.path.dirname(path)) in not_project:
        return extract_project_name(os.path.dirname(path))
    else:
        return os.path.basename(os.path.dirname(path))
    
def emitPythonJob(full_table_name: str, flow_id: str, job_id:str):
    import datahub.emitter.mce_builder as builder
    from datahub.emitter.mcp import MetadataChangeProposalWrapper
    from datahub.metadata.schema_classes import DataFlowInfoClass,DataJobInfoClass

    from datahub.emitter.rest_emitter import DatahubRestEmitter

    # Create an emitter to DataHub over REST
    emitter = DatahubRestEmitter(gms_server="http://staging-ccatalog-gms.cads.live/", extra_headers={})

    # Construct a MetadataChangeProposalWrapper object.
    metadata_event = MetadataChangeProposalWrapper(
        entityUrn=builder.make_data_flow_urn(orchestrator='python', flow_id=flow_id),
        aspect=DataFlowInfoClass(name = flow_id),
    )

    # Emit metadata! This is a blocking call
    emitter.emit(metadata_event)
    
    
    # Construct a MetadataChangeProposalWrapper object.
    metadata_event = MetadataChangeProposalWrapper(
        entityUrn=builder.make_data_job_urn(orchestrator='python', flow_id=flow_id, job_id = job_id),
        aspect=DataJobInfoClass(name = job_id, type='python'),
    )

    # Emit metadata! This is a blocking call
    emitter.emit(metadata_event)
    
    
    # Emit lineage job python and full_table_name
    lineage_mce = builder.make_lineage_mce(
        [
            builder.make_dataset_urn("hive", full_table_name),  # Upstream
        ],
        builder.make_data_job_urn(orchestrator='python', flow_id=flow_id, job_id = job_id),  # Downstream
    )
    
    emitter = DatahubRestEmitter(gms_server="http://staging-ccatalog-gms.cads.live/", extra_headers={})
    emitter.emit(lineage_mce)

