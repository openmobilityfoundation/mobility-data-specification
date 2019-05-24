# Mobility Data Specification: **Standards and Conventions**

This specification contains a list of common standards and conventions used by the various Mobility Data Specifications.

* Authors: LADOT
* Date: 16 May 2019

## Authorization

All MDS APIs require a valid `access_token` to be provided via a [JWT](https://jwt.io/) in the `Authorization` header of each request in the form `Authorization: Bearer <access_token>`. Certain API requests (for example, MDS Agency) expect `provider_id` to be one of the claims in the token. The issuance, expiration and revocation policies for tokens are at the discretion of the Agency.

## Pagination

APIs may decide to paginate the data payload. If so, pagination must comply with the [JSON API](http://jsonapi.org/format/#fetching-pagination) specification:

```
{
	"vehicles": [ ... ]
 	"links": {
        "first": "https://...",
        "last": "https://...",
        "prev": "https://...",
        "next": "https://..."
    }
}
```
