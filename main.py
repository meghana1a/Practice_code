from fastapi import FastAPI, Depends, HTTPException, status
from bson import ObjectId

from database import get_database
from schemas import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse
)

app = FastAPI()


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post(
    "/organizations",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_organization(
    organization: OrganizationCreate,
    db = Depends(get_database)
):
    org_dict = organization.dict()

    result = await db.organizations.insert_one(org_dict)

    return {
        "id": str(result.inserted_id),
        **org_dict
    }

@app.get(
    "/organizations",
    response_model=list[OrganizationResponse]
)
async def get_all_organizations(db=Depends(get_database)):
    organizations = []
    async for org in db.organizations.find():
        organizations.append({
            "id": str(org["_id"]),
            "name": org["name"],
            "industry": org["industry"],
            "size": org["size"]
        })
    return organizations


@app.get(
    "/organizations/{organization_id}",
    response_model=OrganizationResponse
)
async def get_organization_by_id(
    organization_id: str,
    db=Depends(get_database)
):
    org = await db.organizations.find_one({"_id": ObjectId(organization_id)})

    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    return {
        "id": str(org["_id"]),
        "name": org["name"],
        "industry": org["industry"],
        "size": org["size"]
    }


@app.put(
    "/organizations/{organization_id}",
    response_model=OrganizationResponse
)
async def update_organization(
    organization_id: str,
    organization: OrganizationUpdate,
    db=Depends(get_database)
):
    update_data = organization.dict(exclude_none=True)

    result = await db.organizations.update_one(
        {"_id": ObjectId(organization_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Organization not found")

    org = await db.organizations.find_one({"_id": ObjectId(organization_id)})

    return {
        "id": str(org["_id"]),
        "name": org["name"],
        "industry": org["industry"],
        "size": org["size"]
    }



@app.delete(
    "/organizations/{organization_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_organization(
    organization_id: str,
    db=Depends(get_database)
):
    result = await db.organizations.delete_one(
        {"_id": ObjectId(organization_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Organization not found")

    return None
