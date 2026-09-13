.PHONY: setup setup-exe-dev

# Install the skill set for Pi and Claude Code on the local machine.
setup:
	# .pi/agent/skills
	npx skills add ./skills/engineering -a pi -g -y
	npx skills add mattpocock/skills/skills/engineering -a pi -g -y
	npx skills add mattpocock/skills/skills/productivity -a pi -g -y
	# .claude/skills
	npx skills add goofansu/pi-subagent -s herdr-implement-spec -a claude-code -g -y
	# .pi/agent/skills + .claude/skills
	npx skills add boldsoftware/exe.dev -s using-exe-dev -a pi -a claude-code -g -y
	npx skills add cli/cli -s gh -a pi -a claude-code -g -y
	npx skills add cursor/plugins -s technical-writing -s unslop -a pi -a claude-code -g -y
	npx skills add herdrdev/herdr -s herdr -a pi -a claude-code -g -y
	npx skills add humanlayer/skills -s show-me -a pi -a claude-code -g -y
	npx skills add modem-dev/hunk/packages/hunk -s hunk-review -a pi -a claude-code -g -y

# Install the skill set for Pi in exe.dev environments.
setup-exe-dev:
	npx skills add boldsoftware/exe.dev -s using-exe-dev -a pi -g -y
	npx skills add cli/cli -s gh -a pi -g -y
	npx skills add cursor/plugins -s technical-writing -s unslop -a pi -g -y
	npx skills add goofansu/skills/skills/engineering -a pi -g -y
	npx skills add herdrdev/herdr -s herdr -a pi -g -y
	npx skills add humanlayer/skills -s show-me -a pi -g -y
	npx skills add mattpocock/skills/skills/engineering -a pi -g -y
	npx skills add mattpocock/skills/skills/productivity -a pi -g -y
	npx skills add modem-dev/hunk/packages/hunk -s hunk-review -a pi -g -y
