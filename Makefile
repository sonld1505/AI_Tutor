.PHONY: build lint unit integration security quality validate-story tree

build:
	./scripts/build.sh

lint:
	./scripts/lint.sh

unit:
	./scripts/unit-test.sh

integration:
	./scripts/integration-test.sh

security:
	./scripts/security-scan.sh

quality:
	./scripts/quality-gate.sh

# Usage: make validate-story STORY=US-101
validate-story:
	STORY_FILE=safe/stories/$(STORY).yaml ./scripts/validate-story.sh

tree:
	tree -L 3 -I node_modules
