#!/usr/bin/env bash
# =============================================================================
# Symbiotic Factory — OpenFOAM WATER Module Mesh & Run Script
# =============================================================================
# Generates the 3D mesh from the helical stator STL and runs the CFD case.
#
# Prerequisites:
#   - OpenFOAM v2312+ installed
#   - OpenSCAD (to export helical_stator.stl)
#   - Source OpenFOAM: source /opt/openfoam/etc/bashrc
#
# Usage: bash run_cfd.sh
# =============================================================================

set -e

CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATOR_SCAD="../../../../02_WATER_Cycloreactor/hardware/helical_stator.scad"
STATOR_STL="$CASE_DIR/constant/triSurface/helical_stator.stl"

echo "============================================================"
echo "  SYMBIOTIC FACTORY — OpenFOAM Cycloreactor CFD Pipeline"
echo "============================================================"

# Step 1: Generate STL from OpenSCAD (if available)
if command -v openscad &> /dev/null; then
    echo "[1/4] Generating STL from OpenSCAD..."
    mkdir -p "$CASE_DIR/constant/triSurface"
    openscad -o "$STATOR_STL" "$STATOR_SCAD"
else
    echo "[1/4] OpenSCAD not found. Please manually export helical_stator.stl"
    echo "       and place it at: $STATOR_STL"
fi

# Step 2: Generate base mesh
echo "[2/4] Generating base hex mesh with blockMesh..."
cd "$CASE_DIR"
blockMesh

# Step 3: Snap mesh to STL geometry
if [ -f "$STATOR_STL" ]; then
    echo "[3/4] Snapping mesh to helical stator geometry..."
    snappyHexMesh -overwrite
else
    echo "[3/4] Skipping snappyHexMesh (no STL found)"
fi

# Step 4: Run the solver
echo "[4/4] Running multiphaseEulerFoam..."
multiphaseEulerFoam

echo ""
echo "============================================================"
echo "  ✅ CFD simulation complete!"
echo "  Post-process with: paraFoam or foamToVTK"
echo "============================================================"
