import os
import sys
import requests
import time

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
    

def add_lineage(upstreamUrn, downstreamUrn):
    url = 'http://staging-ccatalog-gms.cads.live/api/graphql/'
    query = """
mutation updateLineage {
  updateLineage(
    input: {
      edgesToAdd: [
        {
          downstreamUrn: """ + '"' + downstreamUrn + '"' + """
          upstreamUrn: """ + '"' + upstreamUrn + '"' + """
        }
      ]
      edgesToRemove: []
    }
  )
}
    """
    print(query)
    cookies={''}
    headers = {'X-DataHub-Actor': 'urn:li:corpuser:datahub'}
    json={'query': query}
    r = requests.post(url, headers=headers, json=json)
    return r.json()
    
def emitPythonJob(full_table_name: str, flow_id: str, job_id:str):
    print(flow_id, job_id)
    import datahub.emitter.mce_builder as builder
    from datahub.emitter.mcp import MetadataChangeProposalWrapper
    from datahub.metadata.schema_classes import DataFlowInfoClass,DataJobInfoClass, DataJobInputOutputClass

    from datahub.emitter.rest_emitter import DatahubRestEmitter

    # Create an emitter to DataHub over REST
    emitter = DatahubRestEmitter(gms_server="http://staging-ccatalog-gms.cads.live", extra_headers={'X-DataHub-Actor': 'urn:li:corpuser:datahub'})

    # Add dataflow
    metadata_event = MetadataChangeProposalWrapper(
        entityUrn=builder.make_data_flow_urn(orchestrator='python', flow_id=flow_id, cluster = 'ml'),
        aspect=DataFlowInfoClass(
            name = flow_id,
            customProperties = {"user":"duyvnc",
                               "appId":flow_id,
                               "appName": flow_id
                               }
        ),
    )

    emitter.emit(metadata_event)
    
    
    ############# ADD LINEAGE DATAJOB #############
    metadata_event = MetadataChangeProposalWrapper(
        entityUrn=builder.make_data_job_urn(orchestrator='python', flow_id=flow_id, job_id = job_id, cluster = 'ml'),
        aspect=DataJobInputOutputClass(
            inputDatasets = [],
            outputDatasets= [builder.make_dataset_urn("hive", full_table_name)]
        )
    )
    emitter.emit(metadata_event)
    
    
    ############## Add info DATAJOB ###############
    metadata_event = MetadataChangeProposalWrapper(
        entityUrn=builder.make_data_job_urn(orchestrator='python', flow_id=flow_id, job_id = job_id, cluster = 'ml'),
        aspect=DataJobInputOutputClass(
            inputDatasets = [],
            outputDatasets= [builder.make_dataset_urn("hive", full_table_name)]
        )
    )
    
    emitter.emit(metadata_event)
