from flask import current_app


def add_to_index(index, model):
  payload = {}

  for field in model.__indexing__:
    val = getattr(model, field)
    
    try:
      if hasattr(val, "all"):
        val = [d.to_elastic() for d in val.all()]
    except:
      continue

    payload[field] = val
  
  current_app.elasticsearch.index(index=index, id=model.id, document=payload)

def remove_from_index(index, model):
  current_app.elasticsearch.delete(index=index, id=model.id)
