organizations = []
organization_id_counter: int = 1

class OrganizationsCollection:
    def __init__(self):
        self.organizations = organizations
        self.organizations_count = organization_id_counter
    
    async def add_organization(self, name) -> dict:
        id = self.organizations_count
        organization = {
            "id": id,
            "name": name
        }

        self.organizations.append(organization)
        return organization
    
    async def get_organization(self, id) -> dict:

        for org in organizations:
            if org["id"] == id:
                return org
        return None

    async def get_organizations(self) -> dict:
        return organizations