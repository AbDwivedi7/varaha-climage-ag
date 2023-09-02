from fastapi import APIRouter

from crud.organizations import OrganizationsCollection

router = APIRouter()

@router.get("/organization/add_organization")
async def add_organization(name):
    try:
        organizations_collection = OrganizationsCollection()
        return await organizations_collection.add_organization(name=name)
    except Exception as e:
        raise e

@router.get("/organization/get_organization")
async def get_organization(id: int):
    try:
        organizations_collection = OrganizationsCollection()
        return await organizations_collection.get_organization(id=id)
    except Exception as e:
        raise e

@router.get("/organization/get_organizations")
async def get_organizations():
    try:
        organizations_collection = OrganizationsCollection()
        return await organizations_collection.get_organizations()
    except Exception as e:
        raise e