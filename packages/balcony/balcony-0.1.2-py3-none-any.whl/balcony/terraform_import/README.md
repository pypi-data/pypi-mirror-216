# REAL NOTES

- requires terraform 1.15 + 


https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_filters.html#selecting-json-data-json-queries






--------

# TODO:
- resourceNodeName -> terraform name mapping
- terraform import slug generation from resourceNodeData

----------F

- import slug generation from resourceNodeData
- a way of configuring the 'to' argument







----------

# TODO: provider block optional argument
import {
  provider = aws.europe
  to = aws_instance.example["foo"]
  id = "i-abcd1234"
}
-------

docker build -t bbb . && \
  docker run \
    -v ~/.aws:/root/.aws \
    -e AWS_PROFILE="hepapi" \
    -e AWS_DEFAULT_REGION="eu-west-1" \
    --rm -it bbb \
    terraform-import ec2 Instances
---------
## Plan
- [ ] balcony return value should have metadata
- [x] pydantic model for user input
- [x] when a jmespath selector is given, loop through the results
- [ ] implement the cli command for tf import command
  - [ ] get the provider as a parameter
- [ ] create pydantic model validators for the user input
- [ ] check if the user defined tf import yamls would be looked for 
- [ ] terraform can output to a preset directory
  - decide on a directory
  - always output to that directory
  - ask ppl to mount the volume to that directory if they want the output as file
- [ ] docs
  - [ ] code inline docs
  - [ ] development docs
  - [ ] feature/about docs

