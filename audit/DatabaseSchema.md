# Audit API Database Schemas

The objects stored in Postgresql that are directly related to audits include Audits, Audit Events, and Attachments. An Audit summarizes an investigation into the technical compliance of a provider for a specific device. Audits are composed of Audit Events (e.g., audit start, telemetry recorded, note recorded, etc.) and can optionally link to Attachments (media substantiating the Audit) in a one-to-many relationship established by the Audit Attachments table.

Audits, Audit Events, and Attachments are all stored in their own tables, with foreign keys establishing relationships between the tables. An Audit Attachments table is used for an additional level of indirection between Audits and Attachments.

Table schemas are provided below for reference.

#### Audits
```
Table audits {
      id bigint GENERATED ALWAYS AS IDENTITY,
      audit_trip_id uuid NOT NULL (primary key),
      audit_device_id uuid NOT NULL,
      audit_subject_id varchar(255) NOT NULL,
      provider_id uuid NOT NULL,
      provider_name varchar(127) NOT NULL,
      provider_vehicle_id varchar(255) NOT NULL,
      provider_device_id uuid,
      timestamp bigint NOT NULL,
      deleted bigint,
      recorded bigint NOT NULL
}
```

#### Audit Events
```
Table audit_events {
      id bigint GENERATED ALWAYS AS IDENTITY,
      audit_trip_id uuid NOT NULL (primary key),
      audit_event_id uuid NOT NULL,
      audit_event_type varchar(31) NOT NULL,
      audit_issue_code varchar(31),
      audit_subject_id varchar(255) NOT NULL,
      note varchar(255),
      timestamp bigint NOT NULL (primary key),
      lat double precision NOT NULL,
      lng double precision NOT NULL,
      speed real,
      heading real,
      accuracy real,
      altitude real,
      charge real,
      provider_event_type varchar(31)
      provider_event_type_reason varchar(31)
      provider_event_id bigint (FK to events.id)
      recorded bigint NOT NULL
}
```

#### Attachments
```
Table attachments {
      attachment_id uuid NOT NULL (primary key),
      file_extension varchar(31) NOT NULL,
      recorded bigint NOT NULL
}
```

#### Audit Attachments
```
Table audit_attachments {
      attachment_id uuid NOT NULL (primary key) (FK to attachments.attachment_id),
      audit_trip_id uuid NOT NULL (primary key) (FK to audits.id),
      audit_event_id uuid (FK to audit_events.id),
      recorded bigint NOT NULL
}
```
