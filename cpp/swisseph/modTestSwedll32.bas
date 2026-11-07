Attribute VB_Name = "modTestSwedll32"
'=======================================================================
' Test module for Swiss Ephemeris Visual Basic 32-bit API functions
' DLLFileName       :swedll32.dll
' DLLFileSize       :942,592 bytes
' DLLFileDateTime   :04/08/2021  14:04:22
' DLLFileType       :Dynamic link Library(32Bits)
' DLLFileVersion    :2.10.02
' --------------------------------------------------------------
' ThisFileName      :modTestSwedll32.bas
' Created on        :14.10.2021
' Created by        :D.Senthilathiban (Email:athi_ram@yahoo.com)
'===============================================================
'
' from posting by D.Senthilathiban (Email:athi_ram@yahoo.com) in
' Swiss Ephemeris mailing list
'
' This file is in the Public Domain last updated on 14-Oct-2021
'
' The swedll32.dll file must exist in the same directory as the VB executable,
' or in a system directory where it can be found at runtime
'
' *********************CAUTION/WARNING:*************************************
' Test subroutines are written without any arguments and the required argument
' values for the respective Swiss Ephemeris Visual Basic 32-bit API functions
' are selected randomly as a default in respective subroutines for the purpose
' of testing only. However, the user may do changes as required.
'
' For more/updated details of functions/variables and Return values/Errors
' refer webpage https://www.astro.com/swisseph/swephprg.htm
' Programming interface to the Swiss Ephemeris Manual.
''**************************************************************************
'
'/*
'
'  License conditions
'  ------------------
'
'  This file is distributed with NO WARRANTY OF ANY KIND. No author/contributor
'  or distributor accepts any responsibility for the consequences of using it,
'  or for whether it serves any particular purpose or works at all.
'
'  The License grants you the right to use, copy, modify and redistribute,
'  but only under certain conditions that the File information, author/contributor
'  details and this notice be preserved on all copies.
'
'  The author/contributor have no control or influence over any of
'  the derig oE ty ,es://www.a*sp anfsblic Domasom/swisse)st any arg no all )s
=sDswisse)st 
Ws and this******tPntribnx9nw.a*sp anfsblic Domasom/swisse)st any arg no all )s
=sDsw6
 bpe resioes a ws,. ojDmTY OT.rnsrno a,opies.
'
'  T
Ws e seartg/p**********entribn Lic8rol se)sro*pDigooooooooooooe  swisse)stne  swisse)stne  swisse)s1Lctlrg nrce*****nse /p** anse)stne oa*g  the derifsbliFEutor acce))sro*pDigooo1Nw f0$Dncce)(nsrno a,obfsbliFEuliFEPosailingDigoob*,4eHcP iob*,4eHcuHcPyl******ele:yS
n\ exeUbutigc12Hn*pDigexeUsformationfsbligueionfsbligueionfsbligueionfsbligueionfsbliguobfsbliFEuliFEPosailingDigoob*,4eHcP iob*,4eHcuHcPyl******elfsbliFEublig'  obliga2iob*,4e-S
exeUuiv:SsbliFy
x*tebm 