from fastapi import APIRouter, Security

from crud.organizations import OrganizationsCollection
from crud.auth import (get_current_active_user)

router = APIRouter()

# Route to add organization for Admin Only
@router.get(
    "/organization/add_organization",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])]
)
async def add_organization(name):
    try:
        organizations_collection = OrganizationsCollection()
        return await organizations_collection.add_organization(name=name)
    except Exception as e:
        raise e

# Route to get any Organization for Admin or Users Organization for User
@router.get(
    "/organization/get_organization",
    dependencies=[Security(get_current_active_user, scopes=["user:read"])]
)
async def get_organization(
    id: int,
    current_user = Security(get_current_active_user,scopes=["user:read"]),
):
    try:
        organizations_collection = OrganizationsCollection()
        return await organizations_collection.get_organization(id=id, current_user=current_user)
    except Exception as e:
        raise e

# Route to get All Organization for Admin
@router.get(
    "/organization/get_organizations",
    dependencies=[Security(get_current_active_user, scopes=["admin:read"])]
)
async def get_organizations(current_user = Security(get_current_active_user,scopes=["user:read"])):
    try:
        print(current_user, "hello")
        organizations_collection = OrganizationsCollection()
        return await organizations_collection.get_organizations()
    except Exception as e:
        print(e, "jello")
        raise e