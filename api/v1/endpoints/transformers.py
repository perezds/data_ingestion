from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.transformers_models import TransformersModel
from schemas.transformes_schema import TransformersSchema
from core.deps import get_session

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TransformersSchema)
async def post_transformers(transformers: TransformersSchema, db: AsyncSession = Depends(get_session)):

    novo_personagem = TransformersModel(nome = transformers.nome,
                                        motor = transformers.motor, 
                                        time = transformers.time, 
                                        tipo_transporte = transformers.tipo_transporte,
                                        idade = transformers.idade, 
                                        cor = transformers.cor, 
                                        foto = transformers.cor)
    db.add(novo_personagem)
    await db.commit()

    return novo_personagem

@router.get("/", response_model=List[TransformersSchema])
async def get_transformer (db : AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(TransformersModel)
        result = await session.execute (query)
        personagens: List[TransformersModel] = result.scarlars().all()# type: ignore

        return personagens
    
@router.get("/{transformer_id}", response_model=TransformersSchema)
async def get_transformer(transformer_id: int, db: AsyncSession =Depends(get_session)):
    async with db as session:
        query = select(TransformersModel).filter(TransformersModel.id ==transformer_id)
        result = await session.execute(query)
        transformer = result.scalar_one_or_none()

        if transformer:
            return transformer

        else:
            raise HTTPException(detail="Peresonagem nao enconttrado", status_code=status.HTTP_404_NOT_FOUND)
        

@router.put("/ {transformer_id}", response_model=TransformersSchema)
async def put_transformer(transformer_id: int, transformer = TransformersSchema, db: AsyncSession =Depends(get_session)):
    async with db as session:
        query = select(TransformersModel).filter(TransformersModel.id ==transformer_id)
        result = await session.execute(query)
        transformer_up = result.scalar_one_or_none()

    if transformer_up:
        transformer_up.nome = transformer.nome
        transformer_up.motor = transformer.motor
        transformer_up.time = transformer.time
        transformer_up.tipo_transporte = transformer.tipo_transporte
        transformer_up.idade = transformer.idade
        transformer_up.cor = transformer.cor
        transformer_up.foto = transformer.foto

        await session.commit()
        return transformer_up
    
    else:
       raise HTTPException(detail="Peresonagem nao enconttrado", status_code=status.HTTP_404_NOT_FOUND)
    
@router.delete("/{transformer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transformer(transformer_id: int, db: AsyncSession =Depends(get_session)):
    async with db as session:
        query = select(TransformersModel).filter(TransformersModel.id ==transformer_id)
        result = await session.execute(query)
        transformer_del = result.scalar_one_or_none()


    if transformer_del:
        await session.delete(transformer_del)
        await session.commit()
        return Response(status.HTTP_204_NO_CONTENT)
    
    else:
          raise HTTPException(detail="Peresonagem nao enconttrado", status_code=status.HTTP_404_NOT_FOUND)
