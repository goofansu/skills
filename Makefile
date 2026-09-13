install:
	# .agents/skills 
	npx skills add ./skills/engineering -a codex -g -y
	npx skills add mattpocock/skills/skills/engineering -a codex -g -y
	npx skills add mattpocock/skills/skills/productivity -a codex -g -y
	npx skills add boldsoftware/exe.dev -s using-exe-dev -a codex -g -y
	# .claude/skills
	npx skills add goofansu/pi-subagent -s herdr-implement-spec -a claude-code -g -y
	# .agents/skills + .claude/skills
	npx skills add cli/cli -s gh -a codex -a claude-code -g -y
	npx skills add herdrdev/herdr -s herdr -a codex -a claude-code -g -y
	npx skills add humanlayer/skills -s show-me -a codex -a claude-code -g -y
	npx skills add modem-dev/hunk/packages/hunk -s hunk-review -a codex -a claude-code -g -y
	npx skills add cursor/plugins -s technical-writing -s unslop -a codex -a claude-code -g -y
