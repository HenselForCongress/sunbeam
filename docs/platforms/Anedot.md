# Anedot Platform Documentation

## Webhooks

[Anedot Docs](https://help.anedot.com/en/articles/9038669-webhooks-api)

## Payloads

**Donation**
Example Anedot donation payload

```json
{
  "event": "donation_completed",
  "payload": {
    "submission_id": "f42e7e4f-c93d-4956-a5a2-efab4eef4558",
    "donation": {
      "id": "d467208a8376024eacd71",
      "donation_project": "",
      "products": [
        {
          "internal_identifier": "dl332",
          "name": "Slipper"
        }
      ],
      "fees": {
        "anedot_fees": {
          "amount": "1.30"
        },
        "vendor_fees": []
      }
    },
    "origin": "hosted",
    "commitment_uid": "e1c696e4-4b7d-443b-a69d-1eb1f7027e29",
    "event_amount": "25.00",
    "amount_in_dollars": "25.0",
    "net_amount": "23.70",
    "frequency": "once",
    "action_page_id": "e8f8f185-9a94-4fec-8c9c-974065b4db75",
    "action_page_name": "New Donation Page",
    "donor_profile_id": "",
    "payment_method_id": "9d19c94c-8249-4a26-b1aa-299a423bc852",
    "created_at": "2020-12-11 22:06:25 UTC",
    "updated_at": "2020-12-11 22:06:26 UTC",
    "address_line_1": "143 S 3rd St",
    "address_line_2": "",
    "address_city": "Philadelphia",
    "address_region": "PA",
    "address_postal_code": "19106",
    "address_country": "US",
    "email": "susan.b.anthony@anedot.com",
    "phone": "5552221212",
    "first_name": "Susan",
    "last_name": "Anthony",
    "middle_name": "",
    "occupation": "",
    "employer_name": "",
    "title": "",
    "suffix": "",
    "ip_address": "10.0.0.1",
    "recurring": "true",
    "is_recurring_commitment": "true",
    "referrer": "https://secure.anedot.com/example/slug",
    "referrer_to_form": "",
    "custom_field_responses": {
      "opt_one": "Option One"
    },
    "communications_consent_email": "",
    "communications_consent_phone": "",
    "currently_employed": ""
  }
}
```
