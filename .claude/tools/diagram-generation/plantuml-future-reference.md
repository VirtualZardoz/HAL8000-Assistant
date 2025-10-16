# PlantUML Integration - Future Reference

## Decision Made: 2025-09-19
**Status**: Deferred - Mermaid covers 95%+ of use cases without Java dependency

## Current State
- All 4 diagram types working via Mermaid CLI
- Professional BPMN-style output achieved
- Zero additional dependencies required

## PlantUML Value Proposition
### What PlantUML Would Add:
- **True BPMN 2.0 compliance** (official notation standards)
- **Advanced BPMN elements**:
  - Pools and lanes for complex processes
  - Event types (timer, message, error, escalation)
  - Gateway types (exclusive, inclusive, parallel, event-based)
  - Artifacts (data objects, groups, text annotations)
- **UML diagram types**:
  - Class diagrams for software architecture
  - Sequence diagrams (alternative to Mermaid)
  - Component and deployment diagrams
- **Enterprise-grade compliance** for formal documentation

### Current Mermaid Limitations:
- BPMN-style but not BPMN 2.0 compliant
- Limited advanced BPMN symbols
- No UML class diagram support

## Implementation Requirements (If Needed)
### Prerequisites:
1. **Java Runtime Environment** (JRE 8+)
   ```bash
   # Windows - via Chocolatey
   choco install openjdk

   # Or manual download from Oracle/OpenJDK
   ```

2. **PlantUML JAR file**
   ```bash
   # Download plantuml.jar
   # Place in .claude/context/tools/diagram-generation/bin/
   ```

3. **Script Updates**
   - Update `DIAGRAM_TOOLS` mapping for BPMN
   - Add PlantUML command execution
   - Handle `.puml` file generation

### Code Changes Required:
```python
# In HAL-generate-diagram.py
DIAGRAM_TOOLS = {
    "process-flow": "mermaid",
    "swimlane": "mermaid",
    "bpmn": "plantuml",  # Switch back to PlantUML
    "sipoc": "mermaid"
}

# Add PlantUML execution
elif tool == "plantuml":
    cmd = ["java", "-jar", str(TOOLS_DIR / "bin" / "plantuml.jar"),
           "-t" + output_format, "-o", str(INBOX_DIR), str(source_file)]
```

## Trigger Points for Revisiting
Consider PlantUML integration when:

1. **Enterprise compliance requirement** - Need formal BPMN 2.0 for auditing
2. **Advanced BPMN features needed** - Complex pools/lanes, specialized events
3. **UML architecture diagrams required** - Class diagrams for system design
4. **Client/regulatory standards** - Specific notation compliance required

## Alternative Solutions
Before adding PlantUML dependency, consider:

1. **Online PlantUML services** for occasional advanced diagrams
2. **Mermaid extensions** as they add more BPMN features
3. **Dedicated UML tools** if only UML diagrams are needed
4. **Export to other tools** for final compliance formatting

## Current Recommendation
**Stick with Mermaid-only approach** until hitting specific compliance or advanced feature requirements that justify Java dependency.

**Estimated implementation effort if needed**: 2-3 hours (Java setup + script updates + testing)

---
*This document preserves the analysis and implementation path for future decision-making while maintaining current simplicity.*