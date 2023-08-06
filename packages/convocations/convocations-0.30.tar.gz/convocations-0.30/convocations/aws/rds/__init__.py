from raft import task
from ...base.utils import print_table
from ...base.utils import notice, notice_end
from ..base import AwsTask, yielder


@task(klass=AwsTask)
def rds_instances(ctx, session=None, profile=None, **kwargs):
    """
    shows all rds instances and their endpoints
    """
    rds = session.client('rds')
    instances = rds.describe_db_instances()
    instances = instances['DBInstances']
    header = [ 'name', 'engine', 'endpoint', 'status', ]
    rows = []
    for x in instances:
        rows.append([
            x['DBInstanceIdentifier'],
            f"{x['Engine']} {x['EngineVersion']}",
            f"{x['Endpoint']['Address']}:{x['Endpoint']['Port']}",
            x['DBInstanceStatus'],
        ])
    rows.sort(key=lambda lx: lx[0])
    print_table(header, rows)


@task(klass=AwsTask)
def rds_clusters(ctx, name='', session=None, profile=None, **kwargs):
    """
    shows all rds instances and their endpoints
    """
    rds = session.client('rds')
    clusters = rds.describe_db_clusters()
    name = name.lower()
    clusters = clusters['DBClusters']
    header = [ 'name', 'endpoint', ]
    rows = []
    for x in clusters:
        cluster_name = x['DBClusterIdentifier']
        cluster_name = cluster_name.lower()
        if name in cluster_name:
            rows.append([
                x['DBClusterIdentifier'],
                x['Endpoint'],
            ])
    rows.sort(key=lambda lx: lx[0])
    print_table(header, rows)


@task(klass=AwsTask)
def sys_password(ctx, cluster_name, session=None, profile=None, **kwargs):
    """
    shows the sys password for an custom rds for oracle rac database
    """
    notice('connecting to rds')
    rds = session.client('rds')
    clusters = rds.describe_db_clusters()
    clusters = clusters['DBClusters']
    notice_end()
    notice(cluster_name)
    cluster_name = cluster_name.lower()
    resource_id = None
    for x in clusters:
        st = x['DBClusterIdentifier'].lower()
        if cluster_name == st:
            resource_id = x['DbClusterResourceId']
            notice_end(resource_id)
            break
    if not resource_id:
        return
    notice('looking up sys password')
    secret_name = f'do-not-delete-rds-custom-{resource_id}-sys-'
    sm = session.client('secretsmanager')
    fn = yielder(sm, 'list_secrets', session, Filters=[{
        'Key': 'name',
        'Values': [ secret_name ],
    }])
    notice_end()
    for x in fn:
        name = x['Name']
        response = sm.get_secret_value(SecretId=name)
        print(response['SecretString'])


@task(klass=AwsTask)
def rds_ssh(ctx, name, session=None, profile=None, **kwargs):
    """
    sshes to a custom rds for oracle rac database
    """
    notice('connecting to rds')
    rds = session.client('rds')
    instances = rds.describe_db_instances(Filters=[{
        'Name': 'db-instance-id',
        'Values': [ name ],
    }])
    instances = instances['DBInstances']
    if instances:
        resource_id = instances[0]['DbiResourceId']
        notice_end(resource_id)
    else:
        notice_end('not found')
        return
    from convocations.aws.ec2 import instance_by_name
    from convocations.aws.ec2.ssh import download_secret
    x = instance_by_name(ctx, resource_id, session=session)
    key_name = x.key_name
    username = 'ec2-user'
    ip_address = x.private_ip_address
    notice('key name')
    notice_end(key_name)
    notice('ip address')
    notice_end(ip_address)
    with download_secret(session, x.key_name) as f:
        ssh_cmd = f'ssh -i {f.name} {username}@{ip_address}'
        notice_end(ssh_cmd)
        ctx.run(ssh_cmd, pty=True)
        return
