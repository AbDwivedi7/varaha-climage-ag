organizations = {}
organization_id_counter: int = 2

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
        self.organizations[id] = organization
        global organization_id_counter
        organization_id_counter += 1
        return organization
    
    async def get_organization(self, id) -> dict:
        return organizations[id] if id in organizations else None

    async def get_organizations(self) -> dict:
        return organizations
