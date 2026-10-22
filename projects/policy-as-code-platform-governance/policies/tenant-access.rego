package engineering.tenant_access
import rego.v1

default allow := false

role_permissions := {
  "reader": {"read"},
  "operator": {"read", "restart"},
  "admin": {"read", "restart", "update"},
}

allow if {
  input.subject.tenant == input.resource.tenant
  input.action in role_permissions[input.subject.role]
}
