import io

from tola.assembly.assembly import Assembly
from tola.assembly.format import format_agp, format_tpf
from tola.assembly.fragment import Fragment
from tola.assembly.gap import Gap
from tola.assembly.scaffold import Scaffold

from .utils import strip_leading_spaces


def test_format_agp():
    asm = example_assembly()
    agp = io.StringIO()
    format_agp(asm, agp)
    assert agp.getvalue() == strip_leading_spaces(
        """
        # DESCRIPTION: Generated by PretextView Version 0.2.5
        # HiC MAP RESOLUTION: 8666.611572 bp/texel
        chr1	1	20000	1	W	1	20000	+
        chr1	20001	20100	2	U	100	scaffold	yes	proximity_ligation
        chr1	20101	137013	3	W	23200	140112	-
        chr1	137014	137213	4	U	200	scaffold	yes	proximity_ligation
        chr1	137214	241592	5	W	140113	244491	+
        chr1	241593	485824	6	W	1	244232	?
        chrX	1	11033114755	1	W	1	11033114755	+
        chrX	11033114756	11034414755	2	U	1300000	short_arm	yes	proximity_ligation
        chrX	11034414756	11034414765	3	W	11049229141	11049229150	+
        """,
    )


def test_format_tpf():
    asm = example_assembly()
    tpf = io.StringIO()
    format_tpf(asm, tpf)
    assert tpf.getvalue() == strip_leading_spaces(
        """
        ## DESCRIPTION: Generated by PretextView Version 0.2.5
        ## HiC MAP RESOLUTION: 8666.611572 bp/texel
        ?	scaffold_12:1-20000	chr1	PLUS
        GAP	TYPE-2	100
        ?	scaffold_12:23200-140112	chr1	MINUS
        GAP	TYPE-2	200
        ?	scaffold_12:140113-244491	chr1	PLUS
        ?	scaffold_3:1-244232	chr1	UNKNOWN
        ?	scaffold_7:1-11033114755	chrX	PLUS
        GAP	SHORT-ARM	1300000
        ?	scaffold_7:11049229141-11049229150	chrX	PLUS
        """,
    )


def example_assembly():
    return Assembly(
        name="hap1",
        header=[
            "DESCRIPTION: Generated by PretextView Version 0.2.5",
            "HiC MAP RESOLUTION: 8666.611572 bp/texel",
        ],
        scaffolds=[
            Scaffold(
                name="chr1",
                rows=[
                    Fragment(name="scaffold_12", start=1, end=20000, strand=1),
                    Gap(length=100, gap_type="scaffold"),
                    Fragment(name="scaffold_12", start=23200, end=140112, strand=-1),
                    Gap(length=200, gap_type="scaffold"),
                    Fragment(name="scaffold_12", start=140113, end=244491, strand=1),
                    Fragment(name="scaffold_3", start=1, end=244232, strand=0),
                ],
            ),
            Scaffold(
                name="chrX",
                rows=[
                    Fragment(name="scaffold_7", start=1, end=11033114755, strand=1),
                    Gap(length=1_300_000, gap_type="short_arm"),
                    Fragment(
                        name="scaffold_7", start=11049229141, end=11049229150, strand=1,
                    ),
                ],
            ),
        ],
    )


if __name__ == "__main__":
    test_format_agp()
    test_format_tpf()
