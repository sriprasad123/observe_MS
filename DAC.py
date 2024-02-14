from diagrams import Cluster, Diagram
from diagrams.aws.storage import SimpleStorageServiceS3Bucket
from diagrams.onprem.compute import Server
from diagrams.k8s.compute import Pod
from diagrams.k8s.storage import PV, PVC
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.logging import Loki
from diagrams.onprem.queue import Kafka


with Diagram("Exts exporter flow", show=False):
    with Cluster("MKS cluster"):
        exts=Pod("exts exporter")
        pvc=PVC("pvc")
        fluentbit=Pod("fluentbit")
        exts - pvc - fluentbit
        
    with Cluster("ESM cluster"):
        grafana=Grafana("Grafana")
        loki=Loki("loki")
        datasource=Kafka("loki datasource")
        datasource >> loki >> grafana
        
    s3=SimpleStorageServiceS3Bucket("s3 bucket")
    Server("target1") >> s3
    Server("target2") >> s3
    Server("target3") >> s3
    Server("target4") >> s3
    Server("target5") >> s3
    
    s3 >> exts
    fluentbit >> datasource
    
