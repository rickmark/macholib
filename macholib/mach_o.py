"""
Other than changing the load commands in such a way that they do not
contain the load command itself, this is largely a by-hand conversion
of the C headers.  Hopefully everything in here should be at least as
obvious as the C headers, and you should be using the C headers as a real
reference because the documentation didn't come along for the ride.

Doing much of anything with the symbol tables or segments is really
not covered at this point.

See /usr/include/mach-o and friends.
"""
import time

from macholib.ptypes import *


_CPU_ARCH_ABI64  = 0x01000000

CPU_TYPE_NAMES = {
    -1:     'ANY',
    1:      'VAX',
    6:      'MC680x0',
    7:      'i386',
    _CPU_ARCH_ABI64  | 7:    'x86_64',
    8:      'MIPS',
    10:     'MC98000',
    11:     'HPPA',
    12:     'ARM',
    _CPU_ARCH_ABI64 | 12:     'ARM64',
    13:     'MC88000',
    14:     'SPARC',
    15:     'i860',
    16:     'Alpha',
    18:     'PowerPC',
    _CPU_ARCH_ABI64  | 18:    'PowerPC64',
}

INTEL64_SUBTYPE = {
    3 : "CPU_SUBTYPE_X86_64_ALL",
    4 : "CPU_SUBTYPE_X86_ARCH1"
}

#define CPU_SUBTYPE_INTEL(f, m) ((cpu_subtype_t) (f) + ((m) << 4))
INTEL_SUBTYPE = {
    0 : "CPU_SUBTYPE_INTEL_MODEL_ALL",
    1 : "CPU_THREADTYPE_INTEL_HTT",
    3 : "CPU_SUBTYPE_I386_ALL",
    4 : "CPU_SUBTYPE_486",
    5 : "CPU_SUBTYPE_586",
    8 : "CPU_SUBTYPE_PENTIUM_3",
    9 : "CPU_SUBTYPE_PENTIUM_M",
    10 : "CPU_SUBTYPE_PENTIUM_4",
    11 : "CPU_SUBTYPE_ITANIUM",
    12 : "CPU_SUBTYPE_XEON",
    34 : "CPU_SUBTYPE_XEON_MP",
    42 : "CPU_SUBTYPE_PENTIUM_4_M",
    43 : "CPU_SUBTYPE_ITANIUM_2",
    38 : "CPU_SUBTYPE_PENTPRO",
    40 : "CPU_SUBTYPE_PENTIUM_3_M",
    52 : "CPU_SUBTYPE_PENTIUM_3_XEON",
    102 : "CPU_SUBTYPE_PENTII_M3",
    132 : "CPU_SUBTYPE_486SX",
    166 : "CPU_SUBTYPE_PENTII_M5",
    199 : "CPU_SUBTYPE_CELERON",
    231 : "CPU_SUBTYPE_CELERON_MOBILE"
}

MC680_SUBTYPE = {
    1 : "CPU_SUBTYPE_MC680x0_ALL",
    2 : "CPU_SUBTYPE_MC68040",
    3 : "CPU_SUBTYPE_MC68030_ONLY"
}

MIPS_SUBTYPE = {
    0 : "CPU_SUBTYPE_MIPS_ALL",
    1 : "CPU_SUBTYPE_MIPS_R2300",
    2 : "CPU_SUBTYPE_MIPS_R2600",
    3 : "CPU_SUBTYPE_MIPS_R2800",
    4 : "CPU_SUBTYPE_MIPS_R2000a",
    5 : "CPU_SUBTYPE_MIPS_R2000",
    6 : "CPU_SUBTYPE_MIPS_R3000a",
    7 : "CPU_SUBTYPE_MIPS_R3000"
}

MC98000_SUBTYPE = {
    0 : "CPU_SUBTYPE_MC98000_ALL",
    1 : "CPU_SUBTYPE_MC98601"
}

HPPA_SUBTYPE = {
    0 : "CPU_SUBTYPE_HPPA_7100",
    1 : "CPU_SUBTYPE_HPPA_7100LC"
}

MC88_SUBTYPE = {
    0 : "CPU_SUBTYPE_MC88000_ALL",
    1 : "CPU_SUBTYPE_MC88100",
    2 : "CPU_SUBTYPE_MC88110"
}

SPARC_SUBTYPE = {
    0 : "CPU_SUBTYPE_SPARC_ALL"
}

I860_SUBTYPE = {
    0 : "CPU_SUBTYPE_I860_ALL",
    1 : "CPU_SUBTYPE_I860_860"
}

POWERPC_SUBTYPE = {
    0 : "CPU_SUBTYPE_POWERPC_ALL",
    1 : "CPU_SUBTYPE_POWERPC_601",
    2 : "CPU_SUBTYPE_POWERPC_602",
    3 : "CPU_SUBTYPE_POWERPC_603",
    4 : "CPU_SUBTYPE_POWERPC_603e",
    5 : "CPU_SUBTYPE_POWERPC_603ev",
    6 : "CPU_SUBTYPE_POWERPC_604",
    7 : "CPU_SUBTYPE_POWERPC_604e",
    8 : "CPU_SUBTYPE_POWERPC_620",
    9 : "CPU_SUBTYPE_POWERPC_750",
    10 : "CPU_SUBTYPE_POWERPC_7400",
    11 : "CPU_SUBTYPE_POWERPC_7450",
    100 : "CPU_SUBTYPE_POWERPC_970"
}

ARM_SUBTYPE = {
    0 : "CPU_SUBTYPE_ARM_ALL12",
    5 : "CPU_SUBTYPE_ARM_V4T",
    6 : "CPU_SUBTYPE_ARM_V6",
    7 : "CPU_SUBTYPE_ARM_V5TEJ",
    8 : "CPU_SUBTYPE_ARM_XSCALE",
    9 : "CPU_SUBTYPE_ARM_V7",
    10 : "CPU_SUBTYPE_ARM_V7F",
    12 : "CPU_SUBTYPE_ARM_V7K"
}

VAX_SUBTYPE = {
    0 : "CPU_SUBTYPE_VAX_ALL",
    1 : "CPU_SUBTYPE_VAX780",
    2 : "CPU_SUBTYPE_VAX785",
    3 : "CPU_SUBTYPE_VAX750",
    4 : "CPU_SUBTYPE_VAX730",
    5 : "CPU_SUBTYPE_UVAXI",
    6 : "CPU_SUBTYPE_UVAXII",
    7 : "CPU_SUBTYPE_VAX8200",
    8 : "CPU_SUBTYPE_VAX8500",
    9 : "CPU_SUBTYPE_VAX8600",
    10 : "CPU_SUBTYPE_VAX8650",
    11 : "CPU_SUBTYPE_VAX8800",
    12 : "CPU_SUBTYPE_UVAXIII",
}


def get_cpu_subtype(cpu_type, cpu_subtype):
    st = cpu_subtype & 0x0fffffff

    if cpu_type == 1:
        subtype = VAX_SUBTYPE.get(st, st)
    elif cpu_type == 6:
        subtype = MC680_SUBTYPE.get(st, st)
    elif cpu_type == 7:
        subtype = INTEL_SUBTYPE.get(st, st)
    elif cpu_type == 7 | _CPU_ARCH_ABI64:
        subtype = INTEL64_SUBTYPE.get(st, st)
    elif cpu_type == 8:
        subtype = MIPS_SUBTYPE.get(st, st)
    elif cpu_type == 10:
        subtype = MC98000_SUBTYPE.get(st, st)
    elif cpu_type == 11:
        subtype = HPPA_SUBTYPE.get(st, st)
    elif cpu_type == 12:
        subtype = ARM_SUBTYPE.get(st, st)
    elif cpu_type == 13:
        subtype = MC88_SUBTYPE.get(st, st)
    elif cpu_type == 14:
        subtype = SPARC_SUBTYPE.get(st, st)
    elif cpu_type == 15:
        subtype = I860_SUBTYPE.get(st, st)
    elif cpu_type == 16:
        subtype = MIPS_SUBTYPE.get(st, st)
    elif cpu_type == 18:
        subtype = POWERPC_SUBTYPE.get(st, st)
    elif cpu_type == 18 | _CPU_ARCH_ABI64:
        subtype = POWERPC_SUBTYPE.get(st, st)
    else:
        subtype = str(st)

    return subtype


_MH_EXECUTE_SYM = "__mh_execute_header"
MH_EXECUTE_SYM = "_mh_execute_header"
_MH_BUNDLE_SYM = "__mh_bundle_header"
MH_BUNDLE_SYM = "_mh_bundle_header"
_MH_DYLIB_SYM = "__mh_dylib_header"
MH_DYLIB_SYM = "_mh_dylib_header"
_MH_DYLINKER_SYM = "__mh_dylinker_header"
MH_DYLINKER_SYM = "_mh_dylinker_header"

(
    MH_OBJECT, MH_EXECUTE, MH_FVMLIB, MH_CORE, MH_PRELOAD, MH_DYLIB,
    MH_DYLINKER, MH_BUNDLE, MH_DYLIB_STUB, MH_DSYM
) = range(0x1, 0xb)

(
    MH_NOUNDEFS, MH_INCRLINK, MH_DYLDLINK, MH_BINDATLOAD, MH_PREBOUND,
    MH_SPLIT_SEGS, MH_LAZY_INIT, MH_TWOLEVEL, MH_FORCE_FLAT, MH_NOMULTIDEFS,
    MH_NOFIXPREBINDING, MH_PREBINDABLE, MH_ALLMODSBOUND, MH_SUBSECTIONS_VIA_SYMBOLS,
    MH_CANONICAL, MH_WEAK_DEFINES, MH_BINDS_TO_WEAK, MH_ALLOW_STACK_EXECUTION,
    MH_ROOT_SAFE, MH_SETUID_SAFE, MH_NO_REEXPORTED_DYLIBS, MH_PIE,
    MH_DEAD_STRIPPABLE_DYLIB, MH_HAS_TLV_DESCRIPTORS, MH_NO_HEAP_EXECUTION
) = map((1).__lshift__, range(25))

MH_MAGIC = 0xfeedface
MH_CIGAM = 0xcefaedfe
MH_MAGIC_64 = 0xfeedfacf
MH_CIGAM_64 = 0xcffaedfe

integer_t = p_int32
cpu_type_t = integer_t
cpu_subtype_t = p_uint32

MH_FILETYPE_NAMES = {
    MH_OBJECT:      'relocatable object',
    MH_EXECUTE:     'demand paged executable',
    MH_FVMLIB:      'fixed vm shared library',
    MH_CORE:        'core',
    MH_PRELOAD:     'preloaded executable',
    MH_DYLIB:       'dynamically bound shared library',
    MH_DYLINKER:    'dynamic link editor',
    MH_BUNDLE:      'dynamically bound bundle',
    MH_DYLIB_STUB:  'shared library stub for static linking',
    MH_DSYM:        'symbol information',
}

MH_FILETYPE_SHORTNAMES = {
    MH_OBJECT:      'object',
    MH_EXECUTE:     'execute',
    MH_FVMLIB:      'fvmlib',
    MH_CORE:        'core',
    MH_PRELOAD:     'preload',
    MH_DYLIB:       'dylib',
    MH_DYLINKER:    'dylinker',
    MH_BUNDLE:      'bundle',
    MH_DYLIB_STUB:  'dylib_stub',
    MH_DSYM:        'dsym',
}

MH_FLAGS_NAMES = {
    MH_NOUNDEFS:                'MH_NOUNDEFS',
    MH_INCRLINK:                'MH_INCRLINK',
    MH_DYLDLINK:                'MH_DYLDLINK',
    MH_BINDATLOAD:              'MH_BINDATLOAD',
    MH_PREBOUND:                'MH_PREBOUND',
    MH_SPLIT_SEGS:              'MH_SPLIT_SEGS',
    MH_LAZY_INIT:               'MH_LAZY_INIT',
    MH_TWOLEVEL:                'MH_TWOLEVEL',
    MH_FORCE_FLAT:              'MH_FORCE_FLAT',
    MH_NOMULTIDEFS:             'MH_NOMULTIDEFS',
    MH_NOFIXPREBINDING:         'MH_NOFIXPREBINDING',
    MH_PREBINDABLE:             'MH_PREBINDABLE',
    MH_ALLMODSBOUND:            'MH_ALLMODSBOUND',
    MH_SUBSECTIONS_VIA_SYMBOLS: 'MH_SUBSECTIONS_VIA_SYMBOLS',
    MH_CANONICAL:               'MH_CANONICAL',
    MH_WEAK_DEFINES:            'MH_WEAK_DEFINES',
    MH_BINDS_TO_WEAK:           'MH_BINDS_TO_WEAK',
    MH_ALLOW_STACK_EXECUTION:   'MH_ALLOW_STACK_EXECUTION',
    MH_ROOT_SAFE:               'MH_ROOT_SAFE',
    MH_SETUID_SAFE:             'MH_SETUID_SAFE',
    MH_NO_REEXPORTED_DYLIBS:    'MH_NO_REEXPORTED_DYLIBS',
    MH_PIE:                     'MH_PIE',
    MH_DEAD_STRIPPABLE_DYLIB:   'MH_DEAD_STRIPPABLE_DYLIB',
    MH_HAS_TLV_DESCRIPTORS:     'MH_HAS_TLV_DESCRIPTORS',
    MH_NO_HEAP_EXECUTION:       'MH_NO_HEAP_EXECUTION',
}

MH_FLAGS_DESCRIPTIONS = {
    MH_NOUNDEFS:                'no undefined references',
    MH_INCRLINK:                'output of an incremental link',
    MH_DYLDLINK:                'input for the dynamic linker',
    MH_BINDATLOAD:              'undefined references bound dynamically when loaded',
    MH_PREBOUND:                'dynamic undefined references prebound',
    MH_SPLIT_SEGS:              'split read-only and read-write segments',
    MH_LAZY_INIT:               '(obsolete)',
    MH_TWOLEVEL:                'using two-level name space bindings',
    MH_FORCE_FLAT:              'forcing all imagges to use flat name space bindings',
    MH_NOMULTIDEFS:             'umbrella guarantees no multiple definitions',
    MH_NOFIXPREBINDING:         'do not notify prebinding agent about this executable',
    MH_PREBINDABLE:             'the binary is not prebound but can have its prebinding redone',
    MH_ALLMODSBOUND:            'indicates that this binary binds to all two-level namespace modules of its dependent libraries',
    MH_SUBSECTIONS_VIA_SYMBOLS: 'safe to divide up the sections into sub-sections via symbols for dead code stripping',
    MH_CANONICAL:               'the binary has been canonicalized via the unprebind operation',
    MH_WEAK_DEFINES:            'the final linked image contains external weak symbols',
    MH_BINDS_TO_WEAK:           'the final linked image uses weak symbols',
    MH_ALLOW_STACK_EXECUTION:   'all stacks in the task will be given stack execution privilege',
    MH_ROOT_SAFE:               'the binary declares it is safe for use in processes with uid zero',
    MH_SETUID_SAFE:             'the binary declares it is safe for use in processes when issetugid() is true',
    MH_NO_REEXPORTED_DYLIBS:    'the static linker does not need to examine dependent dylibs to see if any are re-exported',
    MH_PIE:                     'the OS will load the main executable at a random address',
    MH_DEAD_STRIPPABLE_DYLIB:   'the static linker will automatically not create a LC_LOAD_DYLIB load command to the dylib if no symbols are being referenced from the dylib',
    MH_HAS_TLV_DESCRIPTORS:     'contains a section of type S_THREAD_LOCAL_VARIABLES',
    MH_NO_HEAP_EXECUTION:       'the OS will run the main executable with a non-executable heap even on platforms that don\'t require it',
}

class mach_version_helper(Structure):
    _fields_ = (
        ('major', p_ushort),
        ('minor', p_uint8),
        ('rev', p_uint8),
    )
    def __str__(self):
        return '%s.%s.%s' % (self.major, self.minor, self.rev)

class mach_timestamp_helper(p_uint32):
    def __str__(self):
        return time.ctime(self)

def read_struct(f, s, **kw):
    return s.from_fileobj(f, **kw)

class mach_header(Structure):
    _fields_ = (
        ('magic', p_uint32),
        ('cputype', cpu_type_t),
        ('cpusubtype', cpu_subtype_t),
        ('filetype', p_uint32),
        ('ncmds', p_uint32),
        ('sizeofcmds', p_uint32),
        ('flags', p_uint32),
    )
    def _describe(self):
        bit = 1
        flags = self.flags
        dflags = []
        while flags and bit < (1<<32):
            if flags & bit:
                dflags.append({'name': MH_FLAGS_NAMES.get(bit, str(bit)), 'description': MH_FLAGS_DESCRIPTIONS.get(bit, str(bit))})
                flags = flags ^ bit
            bit <<= 1
        return (
            ('magic', int(self.magic)),
            ('cputype_string', CPU_TYPE_NAMES.get(self.cputype, self.cputype)),
            ('cputype', int(self.cputype)),
            ('cpusubtype_string', get_cpu_subtype(self.cputype, self.cpusubtype)),
            ('cpusubtype', int(self.cpusubtype)),
            ('filetype_string', MH_FILETYPE_NAMES.get(self.filetype, self.filetype)),
            ('filetype', int(self.filetype)),
            ('ncmds', self.ncmds),
            ('sizeofcmds', self.sizeofcmds),
            ('flags', dflags),
            ('raw_flags', int(self.flags))
        )

class mach_header_64(mach_header):
    _fields_ = mach_header._fields_ + (('reserved', p_uint32),)

class load_command(Structure):
    _fields_ = (
        ('cmd', p_uint32),
        ('cmdsize', p_uint32),
    )

    def get_cmd_name(self):
        return LC_NAMES.get(self.cmd, self.cmd)

LC_REQ_DYLD = 0x80000000

(
    LC_SEGMENT, LC_SYMTAB, LC_SYMSEG, LC_THREAD, LC_UNIXTHREAD, LC_LOADFVMLIB,
    LC_IDFVMLIB, LC_IDENT, LC_FVMFILE, LC_PREPAGE, LC_DYSYMTAB, LC_LOAD_DYLIB,
    LC_ID_DYLIB, LC_LOAD_DYLINKER, LC_ID_DYLINKER, LC_PREBOUND_DYLIB,
    LC_ROUTINES, LC_SUB_FRAMEWORK, LC_SUB_UMBRELLA, LC_SUB_CLIENT,
    LC_SUB_LIBRARY, LC_TWOLEVEL_HINTS, LC_PREBIND_CKSUM
) = range(0x1, 0x18)

LC_LOAD_WEAK_DYLIB = LC_REQ_DYLD | 0x18

LC_SEGMENT_64 = 0x19
LC_ROUTINES_64 = 0x1a
LC_UUID = 0x1b
LC_RPATH = (0x1c | LC_REQ_DYLD)
LC_CODE_SIGNATURE = 0x1d
LC_CODE_SEGMENT_SPLIT_INFO = 0x1e
LC_REEXPORT_DYLIB = 0x1f | LC_REQ_DYLD
LC_LAZY_LOAD_DYLIB = 0x20
LC_ENCRYPTION_INFO = 0x21
LC_DYLD_INFO = 0x22
LC_DYLD_INFO_ONLY = 0x22 | LC_REQ_DYLD
LC_LOAD_UPWARD_DYLIB = 0x23 | LC_REQ_DYLD
LC_VERSION_MIN_MACOSX = 0x24
LC_VERSION_MIN_IPHONEOS = 0x25
LC_FUNCTION_STARTS = 0x26
LC_DYLD_ENVIRONMENT = 0x27
LC_MAIN = 0x28 | LC_REQ_DYLD
LC_DATA_IN_CODE = 0x29
LC_SOURCE_VERSION = 0x2a
LC_DYLIB_CODE_SIGN_DRS = 0x2b
LC_ENCRYPTION_INFO_64 = 0x2c
LC_LINKER_OPTION = 0x2d


# this is really a union.. but whatever
class lc_str(p_uint32):
    pass

p_str16 = pypackable('p_str16', bytes, '16s')

vm_prot_t = p_int32
class segment_command(Structure):
    _fields_ = (
        ('segname', p_str16),
        ('vmaddr', p_uint32),
        ('vmsize', p_uint32),
        ('fileoff', p_uint32),
        ('filesize', p_uint32),
        ('maxprot', vm_prot_t),
        ('initprot', vm_prot_t),
        ('nsects', p_uint32), # read the section structures ?
        ('flags', p_uint32),
    )

    def describe(self):
        segname = self.segname
        s = {}
        s['segname'] = self.segname.rstrip('\x00')
        s['vmaddr'] = int(self.vmaddr)
        s['vmsize'] = int(self.vmsize)
        s['fileoff'] = int(self.fileoff)
        s['filesize'] = int(self.filesize)
        s['initprot'] = self.get_initial_virtual_memory_protections()
        s['initprot_raw'] = int(self.initprot)
        s['maxprot'] = self.get_max_virtual_memory_protections()
        s['maxprot_raw'] = int(self.maxprot)
        s['nsects'] = int(self.nsects)
        s['flags'] = self.flags
        return s

    def get_initial_virtual_memory_protections(self):
        vm = []
        if self.initprot == 0:
            vm.append("VM_PROT_NONE")
        if self.initprot & 1:
            vm.append("VM_PROT_READ")
        if self.initprot & 2:
            vm.append("VM_PROT_WRITE")
        if self.initprot & 4:
            vm.append("VM_PROT_EXECUTE")
        return vm

    def get_max_virtual_memory_protections(self):
        vm = []
        if self.maxprot == 0:
            vm.append("VM_PROT_NONE")
        if self.maxprot & 1:
            vm.append("VM_PROT_READ")
        if self.maxprot & 2:
            vm.append("VM_PROT_WRITE")
        if self.maxprot & 4:
            vm.append("VM_PROT_EXECUTE")
        return vm

class segment_command_64(Structure):
    _fields_ = (
        ('segname', p_str16),
        ('vmaddr', p_uint64),
        ('vmsize', p_uint64),
        ('fileoff', p_uint64),
        ('filesize', p_uint64),
        ('maxprot', vm_prot_t),
        ('initprot', vm_prot_t),
        ('nsects', p_uint32), # read the section structures ?
        ('flags', p_uint32),
    )

    def describe(self):
        s = {}
        s['segname'] = self.segname.rstrip('\x00')
        s['vmaddr'] = int(self.vmaddr)
        s['vmsize'] = int(self.vmsize)
        s['fileoff'] = int(self.fileoff)
        s['filesize'] = int(self.filesize)
        s['initprot'] = self.get_initial_virtual_memory_protections()
        s['initprot_raw'] = int(self.initprot)
        s['maxprot'] = self.get_max_virtual_memory_protections()
        s['maxprot_raw'] = int(self.maxprot)
        s['nsects'] = int(self.nsects)
        s['flags'] = self.flags
        return s

    def get_initial_virtual_memory_protections(self):
        vm = []
        if self.initprot == 0:
            vm.append("VM_PROT_NONE")
        if self.initprot & 1:
            vm.append("VM_PROT_READ")
        if self.initprot & 2:
            vm.append("VM_PROT_WRITE")
        if self.initprot & 4:
            vm.append("VM_PROT_EXECUTE")
        return vm

    def get_max_virtual_memory_protections(self):
        vm = []
        if self.maxprot == 0:
            vm.append("VM_PROT_NONE")
        if self.maxprot & 1:
            vm.append("VM_PROT_READ")
        if self.maxprot & 2:
            vm.append("VM_PROT_WRITE")
        if self.maxprot & 4:
            vm.append("VM_PROT_EXECUTE")
        return vm


SG_HIGHVM = 0x1
SG_FVMLIB = 0x2
SG_NORELOC = 0x4

class section(Structure):
    _fields_ = (
        ('sectname', p_str16),
        ('segname', p_str16),
        ('addr', p_uint32),
        ('size', p_uint32),
        ('offset', p_uint32),
        ('align', p_uint32),
        ('reloff', p_uint32),
        ('nreloc', p_uint32),
        ('flags', p_uint32),
        ('reserved1', p_uint32),
        ('reserved2', p_uint32),
    )

    def describe(self):
        s = {}
        s['sectname'] = self.sectname.rstrip('\x00')
        s['segname'] = self.segname.rstrip('\x00')
        s['addr'] = int(self.addr)
        s['size'] = int(self.size)
        s['offset'] = int(self.offset)
        s['align'] = int(self.align)
        s['reloff'] = int(self.reloff)
        s['nreloc'] = int(self.nreloc)
        f = {}
        f['type'] = FLAG_SECTION_TYPES[int(self.flags) & 0xff]
        f['attributes'] = []
        for k in FLAG_SECTION_ATTRIBUTES:
            if k & self.flags:
                f['attributes'].append(FLAG_SECTION_ATTRIBUTES[k])
        if not f['attributes']:
            del f['attributes']
        s['flags'] = f
        s['reserved1'] = int(self.reserved1)
        s['reserved2'] = int(self.reserved2)
        return s

    def add_section_data(self, data):
        self.section_data = data

class section_64(Structure):
    _fields_ = (
        ('sectname', p_str16),
        ('segname', p_str16),
        ('addr', p_uint64),
        ('size', p_uint64),
        ('offset', p_uint32),
        ('align', p_uint32),
        ('reloff', p_uint32),
        ('nreloc', p_uint32),
        ('flags', p_uint32),
        ('reserved1', p_uint32),
        ('reserved2', p_uint32),
        ('reserved3', p_uint32),
    )

    def describe(self):
        s = {}
        s['sectname'] = self.sectname.rstrip('\x00')
        s['segname'] = self.segname.rstrip('\x00')
        s['addr'] = int(self.addr)
        s['size'] = int(self.size)
        s['offset'] = int(self.offset)
        s['align'] = int(self.align)
        s['reloff'] = int(self.reloff)
        s['nreloc'] = int(self.nreloc)
        f = {}
        f['type'] = FLAG_SECTION_TYPES[int(self.flags) & 0xff]
        f['attributes'] = []
        for k in FLAG_SECTION_ATTRIBUTES:
            if k & self.flags:
                f['attributes'].append(FLAG_SECTION_ATTRIBUTES[k])
        if not f['attributes']:
            del f['attributes']
        s['flags'] = f
        s['reserved1'] = int(self.reserved1)
        s['reserved2'] = int(self.reserved2)
        s['reserved3'] = int(self.reserved3)
        return s

    def add_section_data(self, data):
        self.section_data = data

SECTION_TYPE = 0xff
SECTION_ATTRIBUTES = 0xffffff00
S_REGULAR = 0x0
S_ZEROFILL = 0x1
S_CSTRING_LITERALS = 0x2
S_4BYTE_LITERALS = 0x3
S_8BYTE_LITERALS = 0x4
S_LITERAL_POINTERS = 0x5
S_NON_LAZY_SYMBOL_POINTERS = 0x6
S_LAZY_SYMBOL_POINTERS = 0x7
S_SYMBOL_STUBS = 0x8
S_MOD_INIT_FUNC_POINTERS = 0x9
S_MOD_TERM_FUNC_POINTERS = 0xa
S_COALESCED = 0xb

FLAG_SECTION_TYPES = {
    0x0 : "S_REGULAR",
    0x1 : "S_ZEROFILL",
    0x2 : "S_CSTRING_LITERALS",
    0x3 : "S_4BYTE_LITERALS",
    0x4 : "S_8BYTE_LITERALS",
    0x5 : "S_LITERAL_POINTERS",
    0x6 : "S_NON_LAZY_SYMBOL_POINTERS",
    0x7 : "S_LAZY_SYMBOL_POINTERS",
    0x8 : "S_SYMBOL_STUBS",
    0x9 : "S_MOD_INIT_FUNC_POINTERS",
    0xa : "S_MOD_TERM_FUNC_POINTERS",
    0xb : "S_COALESCED",
    0xc : "S_GB_ZEROFILL",
    0xd : "S_INTERPOSING",
    0xe : "S_16BYTE_LITERALS",
    0xf : "S_DTRACE_DOF",
    0x10 : "S_LAZY_DYLIB_SYMBOL_POINTERS",
    0x11 : "S_THREAD_LOCAL_REGULAR",
    0x12 : "S_THREAD_LOCAL_ZEROFILL",
    0x13 : "S_THREAD_LOCAL_VARIABLES",
    0x14 : "S_THREAD_LOCAL_VARIABLE_POINTERS",
    0x15 : "S_THREAD_LOCAL_INIT_FUNCTION_POINTERS"
}


FLAG_SECTION_ATTRIBUTES = {
    0x80000000 : "S_ATTR_PURE_INSTRUCTIONS",
    0x40000000 : "S_ATTR_NO_TOC",
    0x20000000 : "S_ATTR_STRIP_STATIC_SYMS",
    0x10000000 : "S_ATTR_NO_DEAD_STRIP",
    0x08000000 : "S_ATTR_LIVE_SUPPORT",
    0x04000000 : "S_ATTR_SELF_MODIFYING_CODE",
    0x02000000 : "S_ATTR_DEBUG",
    0x00000400 : "S_ATTR_SOME_INSTRUCTIONS",
    0x00000200 : "S_ATTR_EXT_RELOC",
    0x00000100 : "S_ATTR_LOC_RELOC"
}

SECTION_ATTRIBUTES_USR = 0xff000000
S_ATTR_PURE_INSTRUCTIONS = 0x80000000
S_ATTR_NO_TOC = 0x40000000
S_ATTR_STRIP_STATIC_SYMS = 0x20000000
SECTION_ATTRIBUTES_SYS = 0x00ffff00
S_ATTR_SOME_INSTRUCTIONS = 0x00000400
S_ATTR_EXT_RELOC = 0x00000200
S_ATTR_LOC_RELOC = 0x00000100


SEG_PAGEZERO =    "__PAGEZERO"
SEG_TEXT =    "__TEXT"
SECT_TEXT =   "__text"
SECT_FVMLIB_INIT0 = "__fvmlib_init0"
SECT_FVMLIB_INIT1 = "__fvmlib_init1"
SEG_DATA =    "__DATA"
SECT_DATA =   "__data"
SECT_BSS =    "__bss"
SECT_COMMON = "__common"
SEG_OBJC =    "__OBJC"
SECT_OBJC_SYMBOLS = "__symbol_table"
SECT_OBJC_MODULES = "__module_info"
SECT_OBJC_STRINGS = "__selector_strs"
SECT_OBJC_REFS = "__selector_refs"
SEG_ICON =     "__ICON"
SECT_ICON_HEADER = "__header"
SECT_ICON_TIFF =   "__tiff"
SEG_LINKEDIT =    "__LINKEDIT"
SEG_UNIXSTACK =   "__UNIXSTACK"

#
#  I really should remove all these _command classes because they
#  are no different.  I decided to keep the load commands separate,
#  so classes like fvmlib and fvmlib_command are equivalent.
#

class fvmlib(Structure):
    _fields_ = (
        ('name', lc_str),
        ('minor_version', mach_version_helper),
        ('header_addr', p_uint32),
    )

class fvmlib_command(Structure):
    _fields_ = fvmlib._fields_

    def describe(self):
        s = {}
        s['header_addr'] = int(self.header_addr)
        return s

class dylib(Structure):
    _fields_ = (
        ('name', lc_str),
        ('timestamp', mach_timestamp_helper),
        ('current_version', mach_version_helper),
        ('compatibility_version', mach_version_helper),
    )

# merged dylib structure
class dylib_command(Structure):
    _fields_ = dylib._fields_

    def describe(self):
        s = {}
        s['timestamp'] = str(self.timestamp)
        s['current_version'] = str(self.current_version)
        s['compatibility_version'] = str(self.compatibility_version)
        return s

class sub_framework_command(Structure):
    _fields_ = (
        ('umbrella', lc_str),
    )

    def describe(self):
        return {}

class sub_client_command(Structure):
    _fields_ = (
        ('client', lc_str),
    )

    def describe(self):
        return {}

class sub_umbrella_command(Structure):
    _fields_ = (
        ('sub_umbrella', lc_str),
    )

    def describe(self):
        return {}

class sub_library_command(Structure):
    _fields_ = (
        ('sub_library', lc_str),
    )

    def describe(self):
        return {}

class prebound_dylib_command(Structure):
    _fields_ = (
        ('name', lc_str),
        ('nmodules', p_uint32),
        ('linked_modules', lc_str),
    )

    def describe(self):
        return {'nmodules': int(self.nmodules)}

class dylinker_command(Structure):
    _fields_ = (
        ('name', lc_str),
    )

    def describe(self):
        return {}

class thread_command(Structure):
    _fields_ = (
        ('flavor', p_uint32),
        ('count', p_uint32)
    )

    def describe(self):
        s = {}
        s['flavor'] = int(self.flavour)
        s['count'] = int(self.count)
        return s

class entry_point_command(Structure):
    _fields_ = (
	    ('entryoff', 	p_uint64),
	    ('stacksize', 	p_uint64),
    )

    def describe(self):
        s = {}
        s['entryoff'] = int(self.entryoff)
        s['stacksize'] = int(self.stacksize)
        return s

class routines_command(Structure):
    _fields_ = (
        ('init_address', p_uint32),
        ('init_module', p_uint32),
        ('reserved1', p_uint32),
        ('reserved2', p_uint32),
        ('reserved3', p_uint32),
        ('reserved4', p_uint32),
        ('reserved5', p_uint32),
        ('reserved6', p_uint32),
    )

    def describe(self):
        s = {}
        s['init_address'] = int(self.init_address)
        s['init_module'] = int(self.init_module)
        s['reserved1'] = int(self.reserved1)
        s['reserved2'] = int(self.reserved2)
        s['reserved3'] = int(self.reserved3)
        s['reserved4'] = int(self.reserved4)
        s['reserved5'] = int(self.reserved5)
        s['reserved6'] = int(self.reserved6)
        return s

class routines_command_64(Structure):
    _fields_ = (
        ('init_address', p_uint64),
        ('init_module', p_uint64),
        ('reserved1', p_uint64),
        ('reserved2', p_uint64),
        ('reserved3', p_uint64),
        ('reserved4', p_uint64),
        ('reserved5', p_uint64),
        ('reserved6', p_uint64),
    )

    def describe(self):
        s = {}
        s['init_address'] = int(self.init_address)
        s['init_module'] = int(self.init_module)
        s['reserved1'] = int(self.reserved1)
        s['reserved2'] = int(self.reserved2)
        s['reserved3'] = int(self.reserved3)
        s['reserved4'] = int(self.reserved4)
        s['reserved5'] = int(self.reserved5)
        s['reserved6'] = int(self.reserved6)
        return s

class symtab_command(Structure):
    _fields_ = (
        ('symoff', p_uint32),
        ('nsyms', p_uint32),
        ('stroff', p_uint32),
        ('strsize', p_uint32),
    )

    def describe(self):
        s = {}
        s['symoff'] = int(self.symoff)
        s['nsyms'] = int(self.nsyms)
        s['stroff'] = int(self.stroff)
        s['strsize'] = int(self.strsize)
        return s


class dysymtab_command(Structure):
    _fields_ = (
        ('ilocalsym', p_uint32),
        ('nlocalsym', p_uint32),
        ('iextdefsym', p_uint32),
        ('nextdefsym', p_uint32),
        ('iundefsym', p_uint32),
        ('nundefsym', p_uint32),
        ('tocoff', p_uint32),
        ('ntoc', p_uint32),
        ('modtaboff', p_uint32),
        ('nmodtab', p_uint32),
        ('extrefsymoff', p_uint32),
        ('nextrefsyms', p_uint32),
        ('indirectsymoff', p_uint32),
        ('nindirectsyms', p_uint32),
        ('extreloff', p_uint32),
        ('nextrel', p_uint32),
        ('locreloff', p_uint32),
        ('nlocrel', p_uint32),
    )

    def describe(self):
        dys = {}
        dys['ilocalsym'] = int(self.ilocalsym)
        dys['nlocalsym'] = int(self.nlocalsym)
        dys['iextdefsym'] = int(self.iextdefsym)
        dys['nextdefsym'] = int(self.nextdefsym)
        dys['iundefsym'] = int(self.iundefsym)
        dys['nundefsym'] = int(self.nundefsym)
        dys['tocoff'] = int(self.tocoff)
        dys['ntoc'] = int(self.ntoc)
        dys['modtaboff'] = int(self.modtaboff)
        dys['nmodtab'] = int(self.nmodtab)
        dys['extrefsymoff'] = int(self.extrefsymoff)
        dys['nextrefsyms'] = int(self.nextrefsyms)
        dys['indirectsymoff'] = int(self.indirectsymoff)
        dys['nindirectsyms'] = int(self.nindirectsyms)
        dys['extreloff'] = int(self.extreloff)
        dys['nextrel'] = int(self.nextrel)
        dys['locreloff'] = int(self.locreloff)
        dys['nlocrel'] = int(self.nlocrel)
        return dys

INDIRECT_SYMBOL_LOCAL = 0x80000000
INDIRECT_SYMBOL_ABS = 0x40000000

class dylib_table_of_contents(Structure):
    _fields_ = (
        ('symbol_index', p_uint32),
        ('module_index', p_uint32),
    )

class dylib_module(Structure):
    _fields_ = (
        ('module_name', p_uint32),
        ('iextdefsym', p_uint32),
        ('nextdefsym', p_uint32),
        ('irefsym', p_uint32),
        ('nrefsym', p_uint32),
        ('ilocalsym', p_uint32),
        ('nlocalsym', p_uint32),
        ('iextrel', p_uint32),
        ('nextrel', p_uint32),
        ('iinit_iterm', p_uint32),
        ('ninit_nterm', p_uint32),
        ('objc_module_info_addr', p_uint32),
        ('objc_module_info_size', p_uint32),
    )

class dylib_module_64(Structure):
    _fields_ = (
        ('module_name', p_uint32),
        ('iextdefsym', p_uint32),
        ('nextdefsym', p_uint32),
        ('irefsym', p_uint32),
        ('nrefsym', p_uint32),
        ('ilocalsym', p_uint32),
        ('nlocalsym', p_uint32),
        ('iextrel', p_uint32),
        ('nextrel', p_uint32),
        ('iinit_iterm', p_uint32),
        ('ninit_nterm', p_uint32),
        ('objc_module_info_size', p_uint32),
        ('objc_module_info_addr', p_uint64),
    )

class dylib_reference(Structure):
    _fields_ = (
        # XXX - ick, fix
        ('isym_flags', p_uint32),
        #('isym', p_uint8 * 3),
        #('flags', p_uint8),
    )

class twolevel_hints_command(Structure):
    _fields_ = (
        ('offset', p_uint32),
        ('nhints', p_uint32),
    )

    def describe(self):
        s = {}
        s['offset'] = int(self.offset)
        s['nhints'] = int(self.nhints)
        return s

class twolevel_hint(Structure):
    _fields_ = (
      # XXX - ick, fix
      ('isub_image_itoc', p_uint32),
      #('isub_image', p_uint8),
      #('itoc', p_uint8 * 3),
  )

class prebind_cksum_command(Structure):
    _fields_ = (
        ('cksum', p_uint32),
    )

    def describe(self):
        return {'cksum': int(self.cksum)}

class symseg_command(Structure):
    _fields_ = (
        ('offset', p_uint32),
        ('size', p_uint32),
    )

    def describe(self):
        s = {}
        s['offset'] = int(self.offset)
        s['size'] = int(self.size)

class ident_command(Structure):
    _fields_ = (
    )

    def describe(self):
        return {}

class fvmfile_command(Structure):
    _fields_ = (
        ('name', lc_str),
        ('header_addr', p_uint32),
    )

    def describe(self):
        return {'header_addr': int(self.header_addr)}

class uuid_command (Structure):
    _fields_ = (
        ('uuid', p_str16),
    )

    def describe(self):
        return {'uuid': self.uuid.rstrip('\x00')}

class rpath_command (Structure):
    _fields_ = (
        ('path', lc_str),
    )

    def describe(self):
        return {}


class linkedit_data_command (Structure):
    _fields_ = (
        ('dataoff',   p_uint32),
        ('datasize', p_uint32),
    )

    def describe(self):
        s = {}
        s['dataoff'] = int(self.dataoff)
        s['datasize'] = int(self.datasize)
        return s


class version_min_command (Structure):
    _fields_ = (
        ('version', p_uint32), # X.Y.Z is encoded in nibbles xxxx.yy.zz
        ('reserved', p_uint32),
    )

    def describe(self):
        v = int(self.version)
        v3 = v & 0xFF
        v = v >> 8
        v2 = v & 0xFF
        v = v >> 8
        v1 = v & 0xFFFF
        return {'version': str(int(v1)) + "." + str(int(v2)) + "." + str(int(v3))}

class source_version_command (Structure):
    _fields_ = (
        ('version',   p_uint64),
    )

    def describe(self):
        v = int(self.version)
        a = v >> 40
        b = (v >> 30) & 0x3ff
        c = (v >> 20) & 0x3ff
        d = (v >> 10) & 0x3ff
        e = v & 0x3ff
        r = str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d)+'.'+str(e)
        return {'version': r}

class encryption_info_command (Structure):
    _fields_ = (
        ('cryptoff',    p_uint32),
        ('cryptsize',   p_uint32),
        ('cryptid',     p_uint32),
    )

    def describe(self):
        s = {}
        s['cryptoff'] = int(self.cryptoff)
        s['cryptsize'] = int(self.cryptsize)
        s['cryptid'] = int(self.cryptid)
        return s

class encryption_info_command_64 (Structure):
    _fields_ = (
        ('cryptoff',    p_uint32),
        ('cryptsize',   p_uint32),
        ('cryptid',     p_uint32),
        ('pad',         p_uint32),
    )

    def describe(self):
        s = {}
        s['cryptoff'] = int(self.cryptoff)
        s['cryptsize'] = int(self.cryptsize)
        s['cryptid'] = int(self.cryptid)
        s['pad'] = int(self.pad)
        return s


class dyld_info_command (Structure):
    _fields_ = (
        ('rebase_off',     p_uint32),
        ('rebase_size',    p_uint32),
        ('bind_off',       p_uint32),
        ('bind_size',      p_uint32),
        ('weak_bind_off',  p_uint32),
        ('weak_bind_size', p_uint32),
        ('lazy_bind_off',  p_uint32),
        ('lazy_bind_size', p_uint32),
        ('export_off',     p_uint32),
        ('export_size',    p_uint32),
    )

    def describe(self):
        dyld = {}
        dyld['rebase_off'] = int(self.rebase_off)
        dyld['rebase_size'] = int(self.rebase_size)
        dyld['bind_off'] = int(self.bind_off)
        dyld['bind_size'] = int(self.bind_size)
        dyld['weak_bind_off'] = int(self.weak_bind_off)
        dyld['weak_bind_size'] = int(self.weak_bind_size)
        dyld['lazy_bind_off'] = int(self.lazy_bind_off)
        dyld['lazy_bind_size'] = int(self.lazy_bind_size)
        dyld['export_off'] = int(self.export_off)
        dyld['export_size'] = int(self.export_size)
        return dyld

class linker_option_command (Structure):
    _fields_ = (
        ('count',         p_uint32),
    )

    def describe(self):
        return {'count': int(self.count)}


LC_REGISTRY = {
    LC_SEGMENT:         segment_command,
    LC_IDFVMLIB:        fvmlib_command,
    LC_LOADFVMLIB:      fvmlib_command,
    LC_ID_DYLIB:        dylib_command,
    LC_LOAD_DYLIB:      dylib_command,
    LC_LOAD_WEAK_DYLIB: dylib_command,
    LC_SUB_FRAMEWORK:   sub_framework_command,
    LC_SUB_CLIENT:      sub_client_command,
    LC_SUB_UMBRELLA:    sub_umbrella_command,
    LC_SUB_LIBRARY:     sub_library_command,
    LC_PREBOUND_DYLIB:  prebound_dylib_command,
    LC_ID_DYLINKER:     dylinker_command,
    LC_LOAD_DYLINKER:   dylinker_command,
    LC_THREAD:          thread_command,
    LC_UNIXTHREAD:      thread_command,
    LC_ROUTINES:        routines_command,
    LC_SYMTAB:          symtab_command,
    LC_DYSYMTAB:        dysymtab_command,
    LC_TWOLEVEL_HINTS:  twolevel_hints_command,
    LC_PREBIND_CKSUM:   prebind_cksum_command,
    LC_SYMSEG:          symseg_command,
    LC_IDENT:           ident_command,
    LC_FVMFILE:         fvmfile_command,
    LC_SEGMENT_64:      segment_command_64,
    LC_ROUTINES_64:     routines_command_64,
    LC_UUID:            uuid_command,
    LC_RPATH:           rpath_command,
    LC_CODE_SIGNATURE:  linkedit_data_command,
    LC_CODE_SEGMENT_SPLIT_INFO:  linkedit_data_command,
    LC_REEXPORT_DYLIB:  dylib_command,
    LC_LAZY_LOAD_DYLIB: dylib_command,
    LC_ENCRYPTION_INFO: encryption_info_command,
    LC_DYLD_INFO:       dyld_info_command,
    LC_DYLD_INFO_ONLY:  dyld_info_command,
    LC_LOAD_UPWARD_DYLIB: dylib_command,
    LC_VERSION_MIN_MACOSX: version_min_command,
    LC_VERSION_MIN_IPHONEOS: version_min_command,
    LC_FUNCTION_STARTS:  linkedit_data_command,
    LC_DYLD_ENVIRONMENT: dylinker_command,
    LC_MAIN: 		entry_point_command,
    LC_DATA_IN_CODE:	linkedit_data_command,
    LC_SOURCE_VERSION:	source_version_command,
    LC_DYLIB_CODE_SIGN_DRS:  linkedit_data_command,
    LC_ENCRYPTION_INFO_64: encryption_info_command_64,
    LC_LINKER_OPTION:  linker_option_command,
}

LC_NAMES = {
    LC_SEGMENT:                     'LC_SEGMENT',
    LC_IDFVMLIB:                    'LC_IDFVMLIB',
    LC_LOADFVMLIB:                  'LC_LOADFVMLIB',
    LC_ID_DYLIB:                    'LC_ID_DYLIB',
    LC_LOAD_DYLIB:                  'LC_LOAD_DYLIB',
    LC_LOAD_WEAK_DYLIB:             'LC_LOAD_WEAK_DYLIB',
    LC_SUB_FRAMEWORK:               'LC_SUB_FRAMEWORK',
    LC_SUB_CLIENT:                  'LC_SUB_CLIENT',
    LC_SUB_UMBRELLA:                'LC_SUB_UMBRELLA',
    LC_SUB_LIBRARY:                 'LC_SUB_LIBRARY',
    LC_PREBOUND_DYLIB:              'LC_PREBOUND_DYLIB',
    LC_ID_DYLINKER:                 'LC_ID_DYLINKER',
    LC_LOAD_DYLINKER:               'LC_LOAD_DYLINKER',
    LC_THREAD:                      'LC_THREAD',
    LC_UNIXTHREAD:                  'LC_UNIXTHREAD',
    LC_ROUTINES:                    'LC_ROUTINES',
    LC_SYMTAB:                      'LC_SYMTAB',
    LC_DYSYMTAB:                    'LC_DYSYMTAB',
    LC_TWOLEVEL_HINTS:              'LC_TWOLEVEL_HINTS',
    LC_PREBIND_CKSUM:               'LC_PREBIND_CKSUM',
    LC_SYMSEG:                      'LC_SYMSEG',
    LC_IDENT:                       'LC_IDENT',
    LC_FVMFILE:                     'LC_FVMFILE',
    LC_SEGMENT_64:                  'LC_SEGMENT_64',
    LC_ROUTINES_64:                 'LC_ROUTINES_64',
    LC_UUID:                        'LC_UUID',
    LC_RPATH:                       'LC_RPATH',
    LC_CODE_SIGNATURE:              'LC_CODE_SIGNATURE',
    LC_CODE_SEGMENT_SPLIT_INFO:     'LC_CODE_SEGMENT_SPLIT_INFO',
    LC_REEXPORT_DYLIB:              'LC_REEXPORT_DYLIB',
    LC_LAZY_LOAD_DYLIB:             'LC_LAZY_LOAD_DYLIB',
    LC_ENCRYPTION_INFO:             'LC_ENCRYPTION_INFO',
    LC_DYLD_INFO:                   'LC_DYLD_INFO',
    LC_DYLD_INFO_ONLY:              'LC_DYLD_INFO_ONLY',
    LC_LOAD_UPWARD_DYLIB:           'LC_LOAD_UPWARD_DYLIB',
    LC_VERSION_MIN_MACOSX:          'LC_VERSION_MIN_MACOSX',
    LC_VERSION_MIN_IPHONEOS:        'LC_VERSION_MIN_IPHONEOS',
    LC_FUNCTION_STARTS:             'LC_FUNCTION_STARTS',
    LC_DYLD_ENVIRONMENT:            'LC_DYLD_ENVIRONMENT',
    LC_MAIN:                        'LC_MAIN',
    LC_DATA_IN_CODE:                'LC_DATA_IN_CODE',
    LC_SOURCE_VERSION:              'LC_SOURCE_VERSION',
    LC_DYLIB_CODE_SIGN_DRS:         'LC_DYLIB_CODE_SIGN_DRS',
}


#this is another union.
class n_un(p_int32):
    pass

class nlist(Structure):
    _fields_ = (
        ('n_un', n_un),
        ('n_type', p_uint8),
        ('n_sect', p_uint8),
        ('n_desc', p_short),
        ('n_value', p_uint32),
    )

class nlist_64(Structure):
    _fields_ = [
        ('n_un',    n_un),
        ('n_type', p_uint8),
        ('n_sect', p_uint8),
        ('n_desc', p_short),
        ('n_value', p_int64),
    ]

N_STAB = 0xe0
N_PEXT = 0x10
N_TYPE = 0x0e
N_EXT = 0x01

N_UNDF = 0x0
N_ABS = 0x2
N_SECT = 0xe
N_PBUD = 0xc
N_INDR = 0xa

NO_SECT = 0
MAX_SECT = 255

REFERENCE_TYPE = 0xf
REFERENCE_FLAG_UNDEFINED_NON_LAZY = 0
REFERENCE_FLAG_UNDEFINED_LAZY = 1
REFERENCE_FLAG_DEFINED = 2
REFERENCE_FLAG_PRIVATE_DEFINED = 3
REFERENCE_FLAG_PRIVATE_UNDEFINED_NON_LAZY = 4
REFERENCE_FLAG_PRIVATE_UNDEFINED_LAZY = 5

REFERENCED_DYNAMICALLY = 0x0010

def GET_LIBRARY_ORDINAL(n_desc):
    return (((n_desc) >> 8) & 0xff)

def SET_LIBRARY_ORDINAL(n_desc, ordinal):
    return (((n_desc) & 0x00ff) | (((ordinal & 0xff) << 8)))

SELF_LIBRARY_ORDINAL = 0x0
MAX_LIBRARY_ORDINAL = 0xfd
DYNAMIC_LOOKUP_ORDINAL = 0xfe
EXECUTABLE_ORDINAL = 0xff

N_DESC_DISCARDED = 0x0020
N_WEAK_REF = 0x0040
N_WEAK_DEF = 0x0080

# /usr/include/mach-o/fat.h
FAT_MAGIC = 0xcafebabe
class fat_header(Structure):
    _fields_ = (
        ('magic', p_uint32),
        ('nfat_arch', p_uint32),
    )

class fat_arch(Structure):
    _fields_ = (
        ('cputype', cpu_type_t),
        ('cpusubtype', cpu_subtype_t),
        ('offset', p_uint32),
        ('size', p_uint32),
        ('align', p_uint32),
    )
