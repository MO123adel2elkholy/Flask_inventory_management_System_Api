#  this query bulider fuction for all modeels
# to apply search and soring and and pginate  returned data


def apply_query(query, args, model):

    page = args.get("page", 1, type=int)
    per_page = min(args.get("per_page", 10, type=int), 50)

    search = args.get("search")

    if search and hasattr(model, "name"):
        query = query.filter(model.name.ilike(f"%{search.strip()}%"))

    sort_by = args.get("sort_by", "id")
    order = args.get("order", "asc")

    if hasattr(model, sort_by):
        column = getattr(model, sort_by)
        query = query.order_by(column.desc() if order == "desc" else column.asc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return pagination  #
