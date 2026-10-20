from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from cosmic_python_anuz.adapters.orm import metadata, start_mapper
from cosmic_python_anuz.config.settings import engine
from cosmic_python_anuz.exceptions.exception import InvalidSku, OutOfStock
from cosmic_python_anuz.models.value_objects import Orderline
from cosmic_python_anuz.services.request_service import AllocateService

# initialize the database
start_mapper()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

async def home(request: Request):
    return JSONResponse({"message": "Hey i am learning cosmic python."})

async def allocate_endpoint(request: Request):
    try:
        body = await request.json()
        if not body:
            raise HTTPException(status_code=400, detail="Something wrong with your payload.")
        reference_id = body.get("reference_id")
        sku = body.get("sku")
        quantity= body.get("quantity")
        line = Orderline(reference_id=reference_id, sku=sku, quantity=quantity)
        batch_ref = await AllocateService(line=line)
        return JSONResponse({"batch_ref": batch_ref})
    except HTTPException:
        raise
    except (OutOfStock, InvalidSku) as e:
        raise HTTPException(status_code=400, detail=f"Out of stock or Invalid SKU, {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong. Try again lol {e}")

routes = [
    Route("/", home, methods=["GET"]),
    Route("/allocate", allocate_endpoint, methods=["POST"])
]


async def lifespan(app):
    await init_db()
    yield


app = Starlette(debug=True, routes=routes, lifespan=lifespan)
