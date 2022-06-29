from flask import current_app


def add_to_index(index, model):
  payload = {}

  for field in model.__indexing__:
    try:
      val = getattr_(model, field)
      if hasattr(val, "all"):
        val = [d.to_elastic() for d in val.all()]
      payload[field] = val
    except:
      continue
  
  current_app.elasticsearch.index(index=index, id=model.id, document=payload)

def remove_from_index(index, model):
  current_app.elasticsearch.delete(index=index, id=model.id)

def getattr_(model, field):
  if "." in field:
    first, last = field.split(".", 1)
    return getattr_(getattr(model, first), last)
  return getattr(model, field)
