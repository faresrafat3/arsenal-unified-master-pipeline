.PHONY: help validate check-links clean

help:
	@echo "⚙️ ARSENAL Unified Master Pipeline"
	@echo "----------------------------------------"
	@echo "Available commands:"
	@echo "  make validate   - Validate the JSON logic inventory"
	@echo "  make check-links- Check for broken markdown links (requires markdown-link-check)"
	@echo "  make clean      - Clean temporary archives or artifacts"

validate:
	@echo "Validating python_logic_inventory.json..."
	@if command -v jq >/dev/null 2>&1; then \
		jq empty python_logic_inventory.json && echo "✅ JSON Logic Inventory is valid."; \
	else \
		echo "⚠️  'jq' is not installed. Please install jq to validate JSON."; \
	fi

clean:
	@echo "Cleaning artifacts..."
	rm -rf *.tmp
