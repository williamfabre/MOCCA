#!/usr/bin/env python

import sys
import symbolic.cmos
from   stratus import *


class Cordic_DP ( Model ):

    def Interface ( self ):
        print 'Cordic_DP.Interface()'
        self.x_p        = SignalIn ( 'x_p',    8 )
        self.y_p        = SignalIn ( 'y_p',    8 )

        self.nx_p       = SignalOut( 'nx_p',   8 )
        self.ny_p       = SignalOut( 'ny_p',   8 )

        self.xmkc_p     = SignalOut( 'xmkc_p', 2 )
        self.ymkc_p     = SignalOut( 'ymkc_p', 2 )
        self.xcmd_p     = SignalOut( 'xcmd_p', 4 )
        self.ymkc_p     = SignalOut( 'ymkc_p', 4 )
        self.i_p        = SignalOut( 'i_p',    4 )

        self.ck         = CkIn     ( 'ck'  )
        self.vdd        = VddIn    ( 'vdd' )
        self.vss        = VddIn    ( 'vss' )
        return


    def Netlist ( self ):
        print 'Cordic_DP.Netlist()'
        # SIGNALS 
        zero_16b            = Signal( 'zero_16b',       16 )
        zero_1b             = Signal( 'zero_1b',         1 )

        n_x                 = Signal( 'n_x',            16 )
        x                   = Signal( 'x',              16 )

        n_y                 = Signal( 'n_y',            16 )
        y                   = Signal( 'y',              16 )

        n_xkc_p_internal_mux        = Signal( 'nxkc_p_internal_mux',        16 )
        n_xkc_p_internal_mux_out    = Signal( 'n_xkc_p_internal_mux_out',   16 )
        n_xkc_p_mux_0               = Signal( 'n_xkc_p_mux_0',              16 )
        n_xkc_p_mux_out_0           = Signal( 'n_xkc_p_mux_out_0',          16 )
        n_xkc_p_mux_1               = Signal( 'n_xkc_p_mux_1',              16 )
        n_xkc_p_mux_out_1           = Signal( 'n_xkc_p_mux_out_1',          16 )
        x_mkc_command               = Signal( 'x_mkc_command',              1  )
        x_signed_overflow_0         = Signal( 'x_signed_overflow_0',        1  )
        x_unsigned_overflow_0       = Signal( 'x_unsigned_overflow_0',      1  )
        n_xkc               = Signal( 'n_xkc',          16 )
        xkc                 = Signal( 'xkc',            16 )


        n_ykc_p_internal_mux        = Signal( 'nukc_p_internal_mux',        16 )
        n_ykc_p_internal_mux_out    = Signal( 'n_ykc_p_internal_mux_out',   16 )
        n_ykc_p_mux_0               = Signal( 'n_ykc_p_mux_0',              16 )
        n_ykc_p_mux_out_0           = Signal( 'n_ykc_p_mux_out_0',          16 )
        n_ykc_p_mux_1               = Signal( 'n_ykc_p_mux_1',              16 )
        n_ykc_p_mux_out_1           = Signal( 'n_ykc_p_mux_out_1',          16 )
        y_mkc_command               = Signal( 'y_mkc_command',              1  )
        y_signed_overflow_0         = Signal( 'x_signed_overflow_1',        1  )
        y_unsigned_overflow_0       = Signal( 'x_unsigned_overflow_1',      1  )
        n_ykc               = Signal( 'n_ykc',          16 )
        ykc                 = Signal( 'ykc',            16 )


        x_sra_1             = Signal( 'x_sra_1',        16 )
        x_sra_2             = Signal( 'x_sra_2',        16 )
        x_sra_3             = Signal( 'x_sra_3',        16 )
        x_sra_4             = Signal( 'x_sra_4',        16 )
        x_sra_5             = Signal( 'x_sra_5',        16 )
        x_sra_6             = Signal( 'x_sra_6',        16 )
        x_sra_7             = Signal( 'x_sra_7',        16 )
        x_sra_1             = Signal( 'x_sra_1',        16 )

        y_sra_1             = Signal( 'y_sra_1',        16 )
        y_sra_2             = Signal( 'y_sra_2',        16 )
        y_sra_3             = Signal( 'y_sra_3',        16 )
        y_sra_4             = Signal( 'y_sra_4',        16 )
        y_sra_5             = Signal( 'y_sra_5',        16 )
        y_sra_6             = Signal( 'y_sra_6',        16 )
        y_sra_7             = Signal( 'y_sra_7',        16 )
        y_sra_1             = Signal( 'y_sra_1',        16 )




        # MASTER CELL
        #######################################################################
        Generate( 'DpgenNmux2'  ,  'nmux2_16b'  , param={'nbit':16,     'behavioral':True,'physical':True,'flags':0} )
        Generate( 'DpgenMux2'   ,  'mux2_16b'   , param={'nbit':16,     'behavioral':True,'physical':True,'flags':0} )
        # Generate( 'DpgenOr2'  ,  'or2'        , param={'nbit': 1,'physical'  :True,'behavioral':True} )
        Generate( 'DpgenOr2'    , 'or2_1'       , param={'nbit': 1,     'physical' : True })
        Generate ( 'DpgenAdsb2f', 'adder_16'    , param={'nbit': 16 ,   'physical' : True })
        Generate ( 'DpgenConst' , 'zero_16b'    , param={ 'nbit': 16,   'const': "0x0000" , 'physical' : True })
        Generate ( 'DpgenConst' , 'zero_1b'     , param={ 'nbit': 1,     'const' : "0b0" , 'physical' : True })

        #######################################################################

        # LISTE DES INSTANCES
        #######################################################################
        self.instances = {}
        #######################################################################



        ############  VALUE 0 ############
        #######################################################################
        self.instances['zero_16b'] = Inst( 'zero_16b', 'zero_16b'
                                          , map = { 'q'   : zero_16b
                                                   , 'vdd' : self.vdd
                                                   , 'vss' : self.vss
                                                   } )
        self.instances['zero_1b'] = Inst( 'zero_1b', 'zero_1b'
                                          , map = { 'q'   : zero_1b
                                                   , 'vdd' : self.vdd
                                                   , 'vss' : self.vss
                                                   } )
        #######################################################################



        ############  MULTIPLEXOR SHIFTER X ############
        ############  MULTIPLEXOR X LAYER 1 ############
        #######################################################################
        self.instances['x_sra_0_0'] = Inst( 'nmux2_16b', 'x_sra_0_0'
                                           , map = { 'cmd' : self.i_p[0]
                                                    , 'i0'  : x
                                                    , 'i1'  : x_sra_1
                                                    , 'nq'  : x_sra_0_0
                                                    , 'vdd' : self.vdd
                                                    , 'vss' : self.vss
                                                    } )

        self.instances['x_sra_0_1'] = Inst( 'nmux2_16b', 'x_sra_0_1'
                                           , map = { 'cmd' : self.i_p[0]
                                                    , 'i0'  : x_sra_2
                                                    , 'i1'  : x_sra_3
                                                    , 'nq'  : x_sra_0_1
                                                    , 'vdd' : self.vdd
                                                    , 'vss' : self.vss
                                                    } )

        self.instances['x_sra_0_3'] = Inst( 'nmux2_16b', 'x_sra_0_3'
                                           , map = { 'cmd' : self.i_p[0]
                                                    , 'i0'  : x_sra_4
                                                    , 'i1'  : x_sra_5
                                                    , 'nq'  : x_sra_0_3
                                                    , 'vdd' : self.vdd
                                                    , 'vss' : self.vss
                                                    } )

        self.instances['x_sra_0_4'] = Inst( 'nmux2_16b', 'x_sra_0_4'
                                           , map = { 'cmd' : self.i_p[0]
                                                    , 'i0'  : x_sra_6
                                                    , 'i1'  : x_sra_7
                                                    , 'nq'  : x_sra_0_4
                                                    , 'vdd' : self.vdd
                                                    , 'vss' : self.vss
                                                    } )

        ############  MULTIPLEXOR X LAYER 2 ############
        self.instances['x_sra_1_0'] = Inst( 'nmux2_16b', 'x_sra_1_0'
                                           , map = { 'cmd' : self.i_p[1]
                                                    , 'i0'  : x_sra_0_0
                                                    , 'i1'  : x_sra_0_1
                                                    , 'nq'  : x_sra_1_0
                                                    , 'vdd' : self.vdd
                                                    , 'vss' : self.vss
                                                    } )

        self.instances['x_sra_1_1'] = Inst( 'nmux2_16b', 'x_sra_1_1'
                                           , map = { 'cmd' : self.i_p[1]
                                                    , 'i0'  : x_sra_0_3
                                                    , 'i1'  : x_sra_0_4
                                                    , 'nq'  : x_sra_1_1
                                                    , 'vdd' : self.vdd
                                                    , 'vss' : self.vss
                                                    } )

        ############  MULTIPLEXOR X LAYER 3 ###########
        self.instances['x_sra_i'] = Inst( 'mux2_16b', 'x_sra_i'
                                         , map = { 'cmd' : self.i_p[2]
                                                  , 'i0'  : x_sra_1_0
                                                  , 'i1'  : x_sra_1_1
                                                  , 'q'  : x_sra_i # pas nq
                                                  , 'vdd' : self.vdd
                                                  , 'vss' : self.vss
                                                  } )
        #######################################################################




        ############  MULTIPLEXOR SHIFTER Y ############
        ############  MULTIPLEXOR Y LAYER 1 ############
        #######################################################################
        self.instances['y_sra_0_0'] = Inst( 'nmux2_16b', 'y_sra_0_0'
                                           , map = { 'cmd'  : self.i_p[0]
                                                    , 'i0'  : y
                                                    , 'i1'  : y_sra_1
                                                    , 'nq'  : y_sra_0_0
                                                    , 'vdd' : self.vdd
                                                    , 'vss' : self.vss
                                                    } )

        self.instances['y_sra_0_1'] = Inst( 'nmux2_16b', 'y_sra_0_1'
                                           , map = { 'cmd'  : self.i_p[0]
                                                    , 'i0'  : y_sra_2
                                                    , 'i1'  : y_sra_3
                                                    , 'nq'  : y_sra_0_1
                                                    , 'vdd' : self.vdd
                                                    , 'vss' : self.vss
                                                    } )

        self.instances['y_sra_0_3'] = Inst( 'nmux2_16b', 'y_sra_0_3'
                                           , map = { 'cmd'  : self.i_p[0]
                                                    , 'i0'  : y_sra_4
                                                    , 'i1'  : y_sra_5
                                                    , 'nq'  : y_sra_0_3
                                                    , 'vdd' : self.vdd
                                                    , 'vss' : self.vss
                                                    } )

        self.instances['y_sra_0_4'] = Inst( 'nmux2_16b', 'y_sra_0_4'
                                           , map = { 'cmd'  : self.i_p[0]
                                                    , 'i0'  : y_sra_6
                                                    , 'i1'  : y_sra_7
                                                    , 'nq'  : y_sra_0_4
                                                    , 'vdd' : self.vdd
                                                    , 'vss' : self.vss
                                                    } )

        ############  MULTIPLEXOR Y LAYER 2 ############
        self.instances['y_sra_1_0'] = Inst( 'nmux2_16b', 'y_sra_1_0'
                                           , map = { 'cmd'  : self.i_p[1]
                                                    , 'i0'  : y_sra_0_0
                                                    , 'i1'  : y_sra_0_1
                                                    , 'nq'  : y_sra_1_0
                                                    , 'vdd' : self.vdd
                                                    , 'vss' : self.vss
                                                    } )

        self.instances['y_sra_1_1'] = Inst( 'nmux2_16b', 'y_sra_1_1'
                                           , map = { 'cmd'  : self.i_p[1]
                                                    , 'i0'  : y_sra_0_3
                                                    , 'i1'  : y_sra_0_4
                                                    , 'nq'  : y_sra_1_1
                                                    , 'vdd' : self.vdd
                                                    , 'vss' : self.vss
                                                    } )

        ############  MULTIPLEXOR Y LAYER 3 ############
        self.instances['y_sra_i']   = Inst( 'mux2_16b', 'y_sra_i'
                                           , map = { 'cmd'  : self.i_p[2]
                                                    , 'i0'  : y_sra_1_0
                                                    , 'i1'  : y_sra_1_1
                                                    , 'q'   : y_sra_i # pas nq
                                                    , 'vdd' : self.vdd
                                                    , 'vss' : self.vss
                                                    } )




        ############  MULTIPLEXOR BEFORE ADD FOR N_XKC ############
        ############  (before n_xkc_p_mux_0) MULTIPLEXOR commanded by xmkc_p LAYER 0 ############
        self.instances['n_xkc_p_internal_mux'] = Inst( 'mux2_16b', 'n_xkc_p_internal_mux'
                                                      , map = { 'cmd'  : self.xmkc_p[0]
                                                               , 'i0'  : x_sra_4
                                                               , 'i1'  : x_sra_5
                                                               , 'q'   : n_xkc_p_internal_mux_out
                                                               , 'vdd' : self.vdd
                                                               , 'vss' : self.vss
                                                               })

        ############  MULTIPLEXOR 0 commanded by xmkc_p LAYER 0 ############
        self.instances['n_xkc_p_mux_0'] = Inst( 'mux2_16b', 'n_xkc_p_mux_0'
                                               , map = { 'cmd'  : self.xmkc_p[1]
                                                        , 'i0'  : x_sra_1
                                                        , 'i1'  : n_xkc_p_internal_mux_out
                                                        , 'q'   : n_xkc_p_mux_out_0
                                                        , 'vdd' : self.vdd
                                                        , 'vss' : self.vss
                                                        })

        self.instances['n_xkc_p_mux_1'] = Inst( 'mux2_16b', 'n_xkc_p_mux_1'
                                               , map = { 'cmd'  : self.xmkc_p
                                                        , 'i0'  : xkc
                                                        , 'i1'  : x_sra_7
                                                        , 'q'   : n_xkc_p_mux_out_1
                                                        , 'vdd' : self.vdd
                                                        , 'vss' : self.vss
                                                        })

        ############  COMMAND MULTIPLEXOR 1 xmkc_p[0] or xmkc_p[1] ############
        self.instances['or2_1']         = Inst ( 'or2_1', 'inst'
                                                , map = { 'i0'  : xmkc_p[1]
                                                         , 'i1'  : xmkc_p[0]
                                                         , 'q'   : xmkc_command
                                                         , 'vdd' : self.vdd
                                                         , 'vss' : self.vss
                                                         })


        ############  MULTIPLEXOR 1 commanded by xmkc_p LAYER 1 ############
        self.instances['n_xkc_p_mux_1'] = Inst( 'mux2_16b', 'n_xkc_p_mux_1'
                                               , map = { 'cmd'  : xmkc_command
                                                        , 'i0'  : xkc
                                                        , 'i1'  : x_sra_7
                                                        , 'q'   : n_xkc_p_mux_out_1
                                                        , 'vdd' : self.vdd
                                                        , 'vss' : self.vss
                                                        })
        ############  ADDER/SUBBER X  ############
        self.instances['x_adder_16_0']     = Inst ( 'adder_16', 'x_adder_16_0'
                                               , map = { 'i0'       : n_xkc_p_mux_out_0
                                                        , 'i1'      : n_xkc_p_mux_out_1
                                                        , 'add_sub' : zero_16b
                                                        , 'q'       : n_xkc
                                                        , 'c30'     : signed_overflow_x
                                                        , 'c31'     : unsigned_overflow_x
                                                        , 'vdd'     : self.vdd
                                                        , 'vss'     : self.vss
                                                        })


        ############  MULTIPLEXOR BEFORE ADD FOR N_YKC ############
        ############  (before n_ykc_p_mux_0) MULTIPLEXOR commanded by ymkc_p LAYER 0 ############
        self.instances['n_ykc_p_internal_mux'] = Inst( 'mux2_16b', 'n_ykc_p_internal_mux'
                                                , map = { 'cmd'  : self.ymkc_p
                                                         , 'i0'  : y_sra_4
                                                         , 'i1'  : y_sra_5
                                                         , 'q'   : n_ykc_p_internal_mux_out
                                                         , 'vdd' : self.vdd
                                                         , 'vss' : self.vss
                                                         })

        self.instances['or2_1']         = Inst ( 'or2_1', 'inst'
                                                , map = { 'i0'  : ymkc_p[1]
                                                         , 'i1'  : ymkc_p[0]
                                                         , 'q'   : ymkc_command
                                                         , 'vdd' : self.vdd
                                                         , 'vss' : self.vss
                                                         })




        ############  MULTIPLEXOR 0 commanded by ymkc_p LAYER 1 ############
        self.instances['n_ykc_p_mux_0'] = Inst( 'mux2_16b', 'n_ykc_p_mux_0'
                                               , map = { 'cmd'  : xmkc_command
                                                        , 'i0'  : y_sra_1
                                                        , 'i1'  : n_ykc_p_internal_mux_out
                                                        , 'q'   : n_ykc_p_mux_out_0
                                                        , 'vdd' : self.vdd
                                                        , 'vss' : self.vss
                                                        })

        ############  COMMAND MULTIPLEXOR 1 ymkc_p[0] or ymkc_p[1] LAYER 2 ############
        self.instances['or2_1']         = Inst ( 'or2_1', 'inst'
                                                , map = { 'i0'  : ymkc_p[1]
                                                         , 'i1'  : ymkc_p[0]
                                                         , 'q'   : ymkc_command
                                                         , 'vdd' : self.vdd
                                                         , 'vss' : self.vss
                                                         })


        ############  MULTIPLEXOR 1 commanded by xmkc_p LAYER 1 ############
        self.instances['n_ykc_p_mux_1'] = Inst( 'mux2_16b', 'n_ykc_p_mux_1'
                                               , map = { 'cmd'  : ymkc_command
                                                        , 'i0'  : ykc
                                                        , 'i1'  : y_sra_7
                                                        , 'q'   : n_ykc_p_mux_out_1
                                                        , 'vdd' : self.vdd
                                                        , 'vss' : self.vss
                                                        })

        ############  ADDER/SUBBER y  ############
        self.instances['y_adder_16_0']     = Inst ( 'adder_16', 'y_adder_16_0'
                                               , map = { 'i0'       : n_ykc_p_mux_out_0
                                                        , 'i1'      : n_ykc_p_mux_out_1
                                                        , 'add_sub' : zero_16b
                                                        , 'q'       : n_ykc
                                                        , 'c30'     : signed_overflow_y
                                                        , 'c31'     : unsigned_overflow_y
                                                        , 'vdd'     : self.vdd
                                                        , 'vss'     : self.vss
                                                        })



        return


    def Layout ( self ):
        print 'Cordic_DP.Layout()'

        # X processing.
        Place     ( self.instances['zero_16b'        ], NOSYM, XY( 0, 0 ) )
        PlaceRight( self.instances['x_sra_0_0'       ], NOSYM )

        # Layout a completer.
        # ...

        return


    def ScriptMain ( **kw ):
        if kw.has_key('editor') and kw['editor']: setEditor( kw['editor'] )

        cordic_dp = Cordic_DP( "cordic_dp" )

        cordic_dp.Interface()
        cordic_dp.Netlist  ()
        cordic_dp.Layout   ()
        cordic_dp.Save     (LOGICAL|PHYSICAL)
        return 1


    if __name__ == "__main__" :
        kw      = {}
        success = ScriptMain( **kw )
        if not success: shellSuccess = 1

        sys.exit( shellSuccess )


