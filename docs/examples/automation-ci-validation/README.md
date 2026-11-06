# Automation deployment documentation examples

These examples accompany a documentation validation exercise. The JSON files
contain placeholders, not production-ready configuration. Replace the model,
repository and approved commit before sending requests to a real installation.

Run `python3 test_examples.py` from this directory. These offline checks verify
example structure and bundle packaging. They do not contact OpenHands, deliver
webhooks, deploy automations, test agent output quality or prove authorization.

Separately, inactive API create, update, retry, rollback and executable-bundle
checks were exercised on automation service 1.19.1. Those authenticated checks
ran from the operator's machine, not GitHub Actions. No OpenHands credential is
stored in this branch or its Actions environment.

The fixture workflow runs only on its task branch. Existing demo workflows and
application source are unchanged. Nothing here should be merged as a production
deployment workflow without engineering review.
