import jwt

meuToken = jwt.encode({'estudos':'python'}, 'programacao', algorithm="HS256")
print(jwt.decode(meuToken, 'programacao', algorithms=['HS256']))

