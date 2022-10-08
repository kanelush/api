from ninja import NinjaAPI
from core.models import Category, Negocios, Contact, Competencia, Producto, Token, PurchaseData, Cart, ECCategoria, ECNegocios, ECProducto, ECContact, ProductoImage
from typing import List
from core.schema import NegocioSchema, NotFoundSchema, ContactSchema, CompetenciaSchema, ProductoSchema, TokenSchema, PurchaseDataSchema, CartSchema, ECCategoriaSchema, ECNegociosSchema, ECProductoSchema, ECContactSchema, ProductoImageSchema
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.common.integration_type import IntegrationType
from django.shortcuts import get_object_or_404

#Init ninja API
api = NinjaAPI()

#TBK
commerce_code = '597043568497'
api_key = '42bdb1c2d4175e67bc45257ac14c03e7'
return_url = "https://chillin.cl/exito"
tx = Transaction(WebpayOptions(commerce_code, api_key, IntegrationType.LIVE))

#API urls

@api.get("/competencias", response=List[CompetenciaSchema])
def competencias(request):
    return Competencia.objects.all()

@api.get("/competencias/{competencia_id}", response={200:CompetenciaSchema, 404:NotFoundSchema})
def competencia(request, competencia_id: int):
    try:
        competencia = Competencia.objects.get(pk=competencia_id)
        return 200, competencia
    except Competencia.DoesNotExist as e:
        return 404, {"message": "Competencia no existe"}

@api.get("/cart", response=List[CartSchema])
def cart(request):
    cart = Cart.objects.all()
    
    return cart

@api.post("/cart", response={201: CartSchema})
def create_cart(request, cart: CartSchema):
    print("print pyhton: ",cart)
    cart = Cart.objects.create(**cart.dict())
    resp = tx.create(cart.buy_order, cart.session_id, cart.total_price, return_url)
    token = resp['token']
    url = resp['url']
    print("resp------>",resp)
    cart.token = token
    cart.url = url
    cart.save()
    print("This is cart ",cart)

    return cart

@api.put("/cart/{cart_id}", response={200: CartSchema, 404:NotFoundSchema})
def update_cart(request, cart_id: int, data: CartSchema):
    try:
        # cart = Cart.objects.get(pk=cart_id)
        cart = get_object_or_404(Cart, id=cart_id)
        print("CART--->", cart.__dict__)
        print("DATAAA---->", data.dict().items())
        for attribute, value in data.dict().items():
             setattr(cart, attribute, value)
             print("atr-->", attribute)
             print("val-->", value)
             print("cartyy-->", cart.buy_order)

        resp = tx.create(cart.buy_order, cart.session_id, cart.total_price, return_url)
        token = resp['token']
        url = resp['url']
        print("IS IT RUNNIN OR NAH?------>iddd",resp)
        cart.token = token
        cart.url = url
        cart.save()
        return 200, cart
    except Cart.DoesNotExist as e:
        return 404, {"message": "Cart no existe"}

@api.get("/cart/{cart_id}", response={200:CartSchema, 404:NotFoundSchema})
def cart_detail(request, cart_id: int):
    try:
        cart = Cart.objects.get(pk=cart_id)
        
        return 200, cart
    except Cart.DoesNotExist as e:
        return 404, {"message": "Cart no existe"}

@api.put("/cart/{cart_id}", response={200: CartSchema, 404:NotFoundSchema})
def update_cart(request, cart_id: int, data: CartSchema):
    try:
        # cart = Cart.objects.get(pk=cart_id)
        cart = get_object_or_404(Cart, id=cart_id)
        print("CART--->", cart.__dict__)
        print("DATAAA---->", data.dict().items())
        for attribute, value in data.dict().items():
             setattr(cart, attribute, value)
             print("atr-->", attribute)
             print("val-->", value)
             print("cartyy-->", cart.buy_order)

        resp = tx.create(cart.buy_order, cart.session_id, cart.total_price, return_url)
        token = resp['token']
        url = resp['url']
        print("IS IT RUNNIN OR NAH?------>iddd",resp)
        cart.token = token
        cart.url = url
        cart.save()
        return 200, cart
    except Cart.DoesNotExist as e:
        return 404, {"message": "Cart no existe"}

@api.post("/contact", response={201: ContactSchema})
def create_contact(request, contact: ContactSchema):
    contact = Contact.objects.create(**contact.dict())
    return contact

@api.get("/contact", response=List[ContactSchema])

def negocios(request):
    return Contact.objects.all()


@api.get("/negocios", response=List[NegocioSchema])
def negocios(request):
    return Negocios.objects.all()

@api.get("/negocios/{negocio_id}", response={200: NegocioSchema, 404:NotFoundSchema})
def negocio(request, negocio_id: int):
    try:
        negocio = Negocios.objects.get(pk=negocio_id)
        return 200, negocio
    except Negocios.DoesNotExist as e:
        return 404, {"message": "Negocio no existe"}

@api.post("/negocios", response={201: NegocioSchema})
def create_negocio(request, negocio: NegocioSchema):
    negocio = Negocios.objects.create(**negocio.dict())
    return negocio

@api.put("/negocios/{negocio_id}", response={200: NegocioSchema, 404:NotFoundSchema})
def change_negocio(request, negocio_id: int, data: NegocioSchema):
    try:
        negocio = Negocios.objects.get(pk=negocio_id)
        for attribute, value in data.dict().items():
             setattr(negocio, attribute, value)
        negocio.save()
        return 200, negocio
    except Negocios.DoesNotExist as e:
        return 404, {"message": "Negocio no existe"}
         
@api.delete("/negocios/{negocio_id}", response={200:None, 404:NotFoundSchema})
def delete_negocio(request, negocio_id: int, data: NegocioSchema):
    try:
        negocio = Negocios.objects.get(pk=negocio_id)
        negocio.delete()
        return 200 
    except Negocios.DoesNotExist as e:
        return 404, {"message": "Negocio no existe"}

@api.get("/productos", response=List[ProductoSchema])
def productos(request):
    productos = Producto.objects.all()
    for transaction in productos:
        resp = tx.create(transaction.buy_order, transaction.session_id, transaction.price, return_url)
        token = resp['token']
        url = resp['url']
        transaction.token = token #guarda token en database
        transaction.url = url #guarda url en database
        transaction.save()        
        print(token)
    return Producto.objects.all()


@api.get("/productos/sorted/{negocio_parent_id}", response=List[ProductoSchema])
def productosfilt(request, negocio_parent_id: int):
    try:
        producto = Producto.objects.filter(negocio_parent_id=negocio_parent_id)
        return 200, producto
    except Producto.DoesNotExist as e:
        return 404, {"message": "Producto no existe"}

@api.get("/productos/{producto_id}", response={200:ProductoSchema, 404:NotFoundSchema})
def producto(request, producto_id: int):
#    productos = Producto.objects.all()
#    for transaction in productos:
#        resp = tx.create(transaction.buy_order, transaction.session_id, transaction.price, return_url)
 #       token = resp['token']
  #      url = resp['url']
   #     transaction.token = token #guarda token en database
    #    transaction.url = url #guarda url en database
     #   transaction.save()        
      #  print(token)

    #return Producto.objects.all()
    try:
        producto = Producto.objects.get(pk=producto_id)
        return 200, producto
    except Producto.DoesNotExist as e:
        return 404, {"message": "Producto no existe"}
#images by foreign key
@api.get("/productos-images", response=List[ProductoImageSchema])
def productos_images(request):
    productos_images = ProductoImage.objects.all()
   
    return ProductoImage.objects.all()


@api.get("/productos-images/sorted/{producto_id}", response=List[ProductoImageSchema])
def productosimgfilt(request, producto_id: int):
    try:
        producto_img = ProductoImage.objects.filter(producto_id=producto_id)
        return 200, producto_img
    except ProductoImage.DoesNotExist as e:
        return 404, {"message": "Producto no existe"}


@api.get("/tokens", response=List[TokenSchema])
def tokens(request):
    return Token.objects.all()

@api.post("/tokens", response={201: TokenSchema})
def create_token(request, token: TokenSchema):
    token_ws = token.token_ws
    token = Token.objects.create(**token.dict())
    print("Podria haber partido x guardar: ", token.token_ws)
    resp = tx.commit(token_ws)
    return token

@api.get("/purchasedata", response=List[PurchaseDataSchema])
def purchasedata(request):
    purchasedata = PurchaseData.objects.all()
    return purchasedata

@api.post("/purchasedata", response={201:PurchaseDataSchema})
def create_purchase(request, purchasedata: PurchaseDataSchema):
    purchasedata = PurchaseData.objects.create(**purchasedata.dict())
    print("This is purchase Data winning winning i feel fantastic and powerful! ",purchasedata)
    return purchasedata



###ENCALBUCO API ROUTES###
@api.get("/encalbuco/negocios", response=List[ECNegociosSchema])
def ecnegocios(request):
    return ECNegocios.objects.all()

@api.get("/encalbuco/negocios/{ecnegocio_id}", response={200: ECNegociosSchema, 404:NotFoundSchema})
def ecnegocio(request, ecnegocio_id: int):
    try:
        ecnegocio = ECNegocios.objects.get(pk=ecnegocio_id)
        return 200, ecnegocio
    except ECNegocios.DoesNotExist as e:
        return 404, {"message": "ECNegocio no existe"}

@api.post("/encalbuco/negocios", response={201: ECNegociosSchema})
def create_ecnegocio(request, ecnegocio: ECNegociosSchema):
    ecnegocio = ECNegocios.objects.create(**ecnegocio.dict())
    return ecnegocio

@api.put("/encalbuco/negocios/{ecnegocio_id}", response={200: ECNegociosSchema, 404:NotFoundSchema})
def change_ecnegocio(request, ecnegocio_id: int, data: ECNegociosSchema):
    try:
        ecnegocio = ECNegocios.objects.get(pk=ecnegocio_id)
        for attribute, value in data.dict().items():
             setattr(ecnegocio, attribute, value)
        ecnegocio.save()
        return 200, ecnegocio
    except ECNegocios.DoesNotExist as e:
        return 404, {"message": "ECNegocio no existe"}
         
@api.delete("/encalbuco/negocios/{ecnegocio_id}", response={200:None, 404:NotFoundSchema})
def delete_ecnegocio(request, ecnegocio_id: int, data: ECNegociosSchema):
    try:
        ecnegocio = ECNegocios.objects.get(pk=ecnegocio_id)
        ecnegocio.delete()
        return 200 
    except ECNegocios.DoesNotExist as e:
        return 404, {"message": "ECNegocio no existe"}

#API ROUTE FOR PRODUCTO
@api.get("/encalbuco/productos", response=List[ECProductoSchema])
def ecproductos(request):
    ecproductos = ECProducto.objects.all()
    return ecproductos

@api.get("/encalbuco/productos/{ecproducto_id}", response={200:ECProductoSchema, 404:NotFoundSchema})
def ecproducto(request, ecproducto_id: int):
    try:
        ecproducto = ECProducto.objects.get(pk=ecproducto_id)
        return 200, ecproducto
    except ECProducto.DoesNotExist as e:
        return 404, {"message": "ECProducto no existe"}

@api.get("/encalbuco/productos/sorted/{ecnegocio_parent}", response=List[ECProductoSchema])
def ecproductosfilt(request, ecnegocio_parent: int):
    try:
        ecproducto = ECProducto.objects.filter(ecnegocio_parent=ecnegocio_parent)
        return 200, ecproducto
    except ECProducto.DoesNotExist as e:
        return 404, {"message": "ECProducto no existe"}


#CONTACT ROUTE API
@api.post("/encalbuco/contact", response={201: ECContactSchema})
def create_eccontact(request, eccontact: ECContactSchema):
    eccontact = ECContact.objects.create(**eccontact.dict())
    return eccontact
