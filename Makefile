install:
	# .agents/skills 
	npx skills add ./skills/engineering -a pi -g -y
	npx skills add mattpocock/skills/skills/engineering -a pi -g -y
	npx skills add mattpocock/skills/skills/productivity -a pi -g -y
	npx skills add boldsoftware/exe.dev -s using-exe-dev -a pi -g -y
	# .claude/skills
	npx skills add goofansu/pi-subagent -s herdr-implement-spec -a claude-code -g -y
	# .agents/skills + .claude/skills
	npx skills add cli/cli -s gh -a pi -a claude-code -g -y
	npx skills add herdrdev/herdr -s herdr -a pi -a claude-code -g -y
	npx skills add humanlayer/skills -s show-me -a pi -a claude-code -g -y
	npx skills add modem-dev/hunk/packages/hunk -s hunk-review -a pi -a claude-code -g -y
	npx skills add cursor/plugins -s technical-writing -s unslop -a pi -a claude-code -g -y
