from fastapi import HTTPException

organizations = {
    1: {
        "name": "Admin Org",
        "id": 1
    }
}
organization_id_counter: int = 2

class OrganizationsCollection:
    def __init__(self):
        self.organizations = organizations
        self.organizations_count = organization_id_counter
    
    # Add Organization CRUD
    async def add_organization(self, name) -> dict:
        try:
            id = self.organizations_count
            organization = {
                "id": id,
                "name": name
            }
            self.organizations[id] = organization
            global organization_id_counter
            organization_id_counter += 1
            return organization
        except Exception:
            raise HTTPException(status_code=400, detail="Something went wrong")
    
    # Get Organization By Id CRUD
    async def get_organization(self, id, current_user:dict) -> dict:
        try:
            if id not in self.organizations:
                return "cant find the organization" # If organization does not exits
            elif current_user["organization_id"] == self.organizations[id]["id"] or current_user["role"] == "admin": # If user is trying to fetch their org or user is admin
                return self.organizations[id]
            else:
                return "Cant find the organization" # If organization does not exits
        except Exception as e:
            raise HTTPException(status_code=400, detail="Something went wrong")

    # Get All Organization CRUD
    async def get_organizations(self) -> dict:
        try:
            # return all organization
            return self.organizations
        except Exception:
            raise HTTPException(status_code=400, detail="Something went wrong")
