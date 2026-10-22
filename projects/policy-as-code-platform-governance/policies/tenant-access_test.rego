package engineering.tenant_access
import rego.v1

test_allow_reader_same_tenant if {
  allow with input as {
    "subject": {"tenant": "tenant-a", "role": "reader"},
    "resource": {"tenant": "tenant-a"},
    "action": "read",
  }
}

test_deny_reader_cross_tenant if {
  not allow with input as {
    "subject": {"tenant": "tenant-a", "role": "reader"},
    "resource": {"tenant": "tenant-b"},
    "action": "read",
  }
}

test_deny_reader_update if {
  not allow with input as {
    "subject": {"tenant": "tenant-a", "role": "reader"},
    "resource": {"tenant": "tenant-a"},
    "action": "update",
  }
}
