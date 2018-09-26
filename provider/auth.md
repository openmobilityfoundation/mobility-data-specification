# Authorization

MDS `providers` **SHALL** provide authorization for API endpoints via a bearer token based auth system. 

For example, the `Authorization` header sent as part of an HTTP request:

```
GET /trips HTTP/1.1
Host: api.provider.co
Authorization: Bearer <token> 
```

More info on how to document [Bearer Auth in swagger](https://swagger.io/docs/specification/authentication/bearer-authentication/)

## JSON Web Tokens

JSON Web Token ([JWT](https://jwt.io/introduction/)) is **RECOMMENDED** as the token format.

JWTs provide a safe, secure way to verify the identity of an agency and provide access to MDS resources without providing access to other, potentially sensitive data.

> JSON Web Token (JWT) is an open standard ([RFC 7519](https://tools.ietf.org/html/rfc7519)) that defines a compact and self-contained way for securely transmitting information between parties as a JSON object. This information can be verified and trusted because it is digitally signed. JWTs can be signed using a secret (with the HMAC algorithm) or a public/private key pair using RSA or ECDSA.

MDS `providers` **MAY** include any metadata in the JWT they wish that helps to route, log, permission, or debug agency requests, leaving their internal implementation flexible.

JWT provides a helpful [debugger](https://jwt.io/#debugger) for testing your token and verifying security.
