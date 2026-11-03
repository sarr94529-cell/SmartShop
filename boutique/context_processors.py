def cart_count(request):
    panier=request.session.get('panier',{})
    return {'cart_count':sum(v for v in panier.values() if isinstance(v,int) and v>0)}
