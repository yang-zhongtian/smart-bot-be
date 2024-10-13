from typing import List
from ninja import Router

from .models import Host
from .schema import HostSchema, StatusSchema, FaceRecordSchema

router = Router()


@router.get('/', response=List[HostSchema])
def host_list(request):
    hosts = Host.objects.all()
    data = []
    for host in hosts:
        status = StatusSchema(
            cam=host.status_cam,
            command=host.status_command,
            analyze=host.status_analyze
        )
        schema = HostSchema(
            id=host.id,
            name=host.name,
            status=status
        )
        data.append(schema)
    return data


@router.get('/{host_id}', response=HostSchema)
def host_detail(request, host_id: str):
    host = Host.objects.get(id=host_id)
    status = StatusSchema(
        cam=host.status_cam,
        command=host.status_command,
        analyze=host.status_analyze
    )
    schema = HostSchema(
        id=host.id,
        name=host.name,
        status=status
    )
    return schema


@router.get('/{host_id}/history', response=List[FaceRecordSchema])
def face_history(request, host_id: str):
    host = Host.objects.get(id=host_id)
    return host.facedetectionrecord_set.all().order_by('-created_at')


@router.get('/{host_id}/history/latest', response=FaceRecordSchema)
def face_latest(request, host_id: str):
    host = Host.objects.get(id=host_id)
    return host.facedetectionrecord_set.latest('created_at')
