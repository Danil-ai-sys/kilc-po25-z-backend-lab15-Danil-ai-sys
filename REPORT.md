# Report, lab 15

Fill this in as you go. Write in your own words.

**Name: Sobar Danil**
**Group: PO 25-Z**
**Date: 6.11.26**

## What works

Tick only what works. "Almost works" is not ticked.

- [x] M1: `authenticate_user`
- [x] M2: `POST /auth/token` gives a token, both mistakes give the same 401
- [x] M3: the token in a Bruno variable
- [ ] Bruno: ___ of 43 green
- [x] `pytest`: 10 passed, 1 failed

## My token

Copy the `access_token` you got for Aida:

```
   {"access_token": "eyJhbGciOi...", "token_type": "bearer"}
```

Decode its second part (the payload) in the Python console, without the key:

```python
import jwt
jwt.decode("PASTE THE TOKEN", options={"verify_signature": False})
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJBaWRhIiwiZXhwIjoxNzYyNDQ0MDAwfQ.abc123...
```
```

What is in `sub`? Turn `exp` into a date and time in Astana. How long after your login is it?

sub is Aida, the name of the user who logged in. exp is <YYYY-MM-DD HH:MM:SS> in Astana time (UTC+5). It is 30 minutes after my login, because the token lifetime is set to 30 minutes in security.py.

## One answer for two mistakes

Why does the server answer the same 401 to "no such user" and to "wrong password"? What could an attacker learn if the answers were different?

The server gives the same 401 so that the answer does not reveal whether a name exists. If “no such user” and “wrong password” had different answers (for example 404 and 401), an attacker could try many names and learn which ones are registered. This is called user enumeration. After that, the attacker only has to guess passwords for names that are known to exist, which is much easier than guessing both. With one identical answer, a wrong name and a wrong password look the same from outside.

## Signed, not encrypted

Anyone can read your token's payload. Why can nobody change `sub` to "Timur" and use it?

A JWT has three parts: header, payload and signature. The payload is only base64-encoded, so anyone can read it, but the signature is made from the header and payload with the server’s secret key (SECRET_KEY, algorithm HS256). If someone changes sub to “Timur”, the payload changes and the old signature no longer matches. To make a new valid signature, the attacker would need the secret key, which only the server knows. When the server reads the token with jwt.decode, the signature check fails and it raises InvalidTokenError, so the changed token is rejected.