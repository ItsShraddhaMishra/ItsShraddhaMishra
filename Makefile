.PHONY: github_readme full_update clean_stale_assets fix_svg_corruption fetch_contributions fetch_scholar compile_readme_assets generate_readme_assets postprocess_generated_assets validate_svgs  clean_generated svg_crusader

PYTHON ?= python3

ASSET_DIR := assets

SVG_GENERATORS := make_readme_assets.py \
	make_identity_panel.py \
	make_system_status_panel.py \
	make_current_mission_panel.py \
	make_tech_stack_panel.py \
	make_featured_projects_panel.py \
	make_publication_panel.py \
	make_tron_contributions.py \
	ares_tron_theme.py

LEGACY_REPAIR_GENERATORS := make_readme_assets.py \
	make_identity_panel.py \
	make_system_status_panel.py \
	make_current_mission_panel.py \
	make_tech_stack_panel.py \
	make_featured_projects_panel.py \
	make_publication_panel.py

CONTRIBUTION_SCRIPTS := fetch_contributions.py \
	make_tron_contributions.py

SCHOLAR_SCRIPTS := fetch_scholar_publications.py \
	update_publications_readme.py

ALL_PY_SCRIPTS := $(SVG_GENERATORS) $(SCHOLAR_SCRIPTS) $(CONTRIBUTION_SCRIPTS) svg_crusader.py


github_readme: clean_stale_assets fix_svg_corruption compile_readme_assets fetch_contributions generate_readme_assets postprocess_generated_assets validate_svgs 
	@echo ""
	@echo "GitHub README assets generated and validated."


full_update: clean_stale_assets fix_svg_corruption compile_readme_assets fetch_contributions fetch_scholar generate_readme_assets postprocess_generated_assets validate_svgs 
	@echo ""
	@echo "Full README update completed, including Google Scholar data."


clean_stale_assets:
	@echo "Clearing stale generated SVG assets before rebuild..."
	@mkdir -p $(ASSET_DIR)
	@rm -f $(ASSET_DIR)/*.svg
	@echo "Stale SVG assets cleared."


fix_svg_corruption:
	@echo "Fixing common SVG/Python corruption patterns..."
	@echo "Repairing legacy generator corruption patterns..."
	@for f in $(LEGACY_REPAIR_GENERATORS); do \
		if [ -f $$f ]; then \
			echo "Repairing $$f"; \
			perl -0pi -e 'sub c { "class" . chr(61) . chr(34) . $$_[0] . chr(34) } \
				s/className=ss="puls/c("pulse")/eg; \
				s/className=nnn/c("scan")/eg; \
				s/className=hhh/c("dash")/eg; \
				s/className=eee\s+panelPulse/c("fadeIn1 panelPulse")/eg; \
				s/className=eIn1\s+panelPulse/c("fadeIn1 panelPulse")/eg; \
				s/className=eIn1/c("fadeIn1")/eg; \
				s/className=eIn2/c("fadeIn2")/eg; \
				s/className=eIn3/c("fadeIn3")/eg; \
				s/className=eIn4/c("fadeIn4")/eg; \
				s/className=tFloat/c("softFloat")/eg; \
				s/className=edge/c("edge")/eg; \
				s/className=eee/c("lineFlow")/eg; \
				s/className=KKK=ddd/c("{fade_class}")/eg; \
				s/\bclass\s*=\s*ss="puls/c("pulse")/eg; \
				s/\bclass\s*=\s*nnn/c("scan")/eg; \
				s/\bclass\s*=\s*hhh/c("dash")/eg; \
				s/\bclass\s*=\s*eee\s+panelPulse/c("fadeIn1 panelPulse")/eg; \
				s/\bclass\s*=\s*eIn1\s+panelPulse/c("fadeIn1 panelPulse")/eg; \
				s/\bclass\s*=\s*eIn1/c("fadeIn1")/eg; \
				s/\bclass\s*=\s*eIn2/c("fadeIn2")/eg; \
				s/\bclass\s*=\s*eIn3/c("fadeIn3")/eg; \
				s/\bclass\s*=\s*eIn4/c("fadeIn4")/eg; \
				s/\bclass\s*=\s*tFloat/c("softFloat")/eg; \
				s/\bclass\s*=\s*edge/c("edge")/eg; \
				s/\bclass\s*=\s*eee/c("lineFlow")/eg; \
				s/\bclass\s*=\s*scan/c("scan")/eg; \
				s/\bclass\s*=\s*dash/c("dash")/eg; \
				s/\bclass\s*=\s*pulse/c("pulse")/eg; \
				s/\bclass\s*=\s*lineFlow/c("lineFlow")/eg; \
				s/\bclass\s*=\s*panelPulse/c("panelPulse")/eg; \
				s/\bclass\s*=\s*softFloat/c("softFloat")/eg;' $$f; \
		fi; \
	done
	@echo "Running SVG Crusader source repair..."
	@$(PYTHON) svg_crusader.py repair
	@echo "Corruption repair pass complete."


compile_readme_assets:
	@echo "Compiling Python asset generators..."
	@for f in $(ALL_PY_SCRIPTS); do \
		if [ -f $$f ]; then \
			echo "Compiling $$f"; \
			$(PYTHON) -m py_compile $$f; \
		else \
			echo "Missing $$f"; \
			exit 1; \
		fi; \
	done
	@echo "Python compile check passed."


fetch_contributions:
	@echo "Fetching GitHub contribution data..."
	@mkdir -p data
	@$(PYTHON) fetch_contributions.py
	@echo "Contribution data updated."


fetch_scholar:
	@echo "Fetching Google Scholar publications..."
	@$(PYTHON) make_publication_panel.py
	@$(PYTHON) update_publications_readme.py
	@echo "Scholar publications updated."


generate_readme_assets:
	@echo "Generating README SVG assets..."
	@$(PYTHON) make_readme_assets.py
	@$(PYTHON) make_identity_panel.py
	@$(PYTHON) make_system_status_panel.py
	@$(PYTHON) make_current_mission_panel.py
	@$(PYTHON) make_tech_stack_panel.py
	@$(PYTHON) make_featured_projects_panel.py
	@$(PYTHON) make_publication_panel.py
	@$(PYTHON) fetch_contributions.py
	@$(PYTHON) make_tron_contributions.py
	@echo "Asset generation complete."


postprocess_generated_assets:
	@echo "Post-processing generated SVG assets..."
	@$(PYTHON) svg_crusader.py repair
	@echo "Generated SVG post-processing complete."


validate_svgs:
	@echo "Validating SVG XML..."
	@$(PYTHON) svg_crusader.py repair
	@$(PYTHON) validate_svgs.py
	@$(PYTHON) svg_crusader.py validate
	@echo "SVG validation passed."




svg_crusader:
	@$(PYTHON) svg_crusader.py all


clean_generated:
	@echo "Removing generated SVG assets..."
	@rm -f $(ASSET_DIR)/*.svg
	@echo "Generated assets removed."
