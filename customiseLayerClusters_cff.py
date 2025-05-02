import FWCore.ParameterSet.Config as cms
from RecoLocalCalo.HGCalRecProducers.hgcalLayerClusters_cff import hgcalLayerClustersEE, hgcalLayerClustersHSi, hgcalLayerClustersHSci
from math import sqrt

def settings(density:str="high",option:int=0,verbose:bool=False):

    assert density == "high" or density == "low", f"Unknown value! density='{density:s}'"
    assert option >= 0 and option <=5, f"Unknown value! option='{option:s}'"

    # Useful distances
    wafer_size = 16.74408 # [cm] wafer_size/12 = 3s
    side = wafer_size / 12. / 3. if density == "high" else wafer_size / 8. / 3. # "low"
    f2f = side * sqrt(3.) # f2f = side * 1/tan(pi/6) == side * sqrt(3)

    # Available delta_c settings (previous "nominal" value was "1.3")
    # HD (eta=2.50): 0 = 0.8056 ("0.8"), 1 = 1.3953 ("1.3"), 4 = 2.4168 ("2.4")
    # LD (eta=1.75): 0 = 1.2084 ("1.2"), 1 = 2.0930 ("1.3"), 2 = 2.4168 ("2.4")
    settings = {
        0: {"radius": 1.*f2f, "ncell": 7, "desc":"1f"},
        1: {"radius": 3.*side, "ncell":13, "desc":"3s"},
        2: {"radius": 2.*f2f, "ncell":19, "desc":"2f"},
        3: {"radius": sqrt( (4.5*side)**2. + (0.5*f2f)**2. ), "ncell":31, "desc":"sqrt((4.5s)^2 + (0.5f)^2)"},
        4: {"radius": 3.*f2f, "ncell":37, "desc":"3f"},
    }

    if option in settings.keys():
        dct = settings[option]
        if verbose:
            print( "########################")
            print( "[customiseLayerClusters]")
            print(f"density: '{density:s}'")
            print(f"option:   {option:.0f}")
            print(f"side:     {side:6.4f} cm")
            print(f"f2f:      {f2f:6.4f} cm")
            print(f"delta_c:  {dct['radius']:6.4f} cm")
            print( "########################")
        return dct
    else:
        raise ValueError(f"Option not found! option='{option}'")

def customiseLayerClusters(process,density:str="high",option:int=0,verbose:bool=False):

    deltac = 1.3
    deltao = 2.6
    dct = settings(density,option,verbose)
    epsilon = 0.1 # cm
    deltac = dct["radius"] - epsilon

    process.hgcalLayerClustersEE.plugin.deltac   = cms.vdouble(deltac, deltac, deltac, 0.0315)
    process.hgcalLayerClustersEE.plugin.deltao   = cms.vdouble(deltao, deltao, deltao, deltao)
    process.hgcalLayerClustersHSi.plugin.deltac  = cms.vdouble(deltac, deltac, deltac, 0.0315)
    process.hgcalLayerClustersHSi.plugin.deltao  = cms.vdouble(deltao, deltao, deltao, deltao)
    process.hgcalLayerClustersHSci.plugin.deltac = cms.vdouble(deltac, deltac, deltac, 0.0315)
    process.hgcalLayerClustersHSci.plugin.deltao = cms.vdouble(deltao, deltao, deltao, deltao)

    return process

def customiseCloseBy(process,density:str="high",verbose:bool=False):

    assert density == "high" or density == "low", f"Unknown value! density='{density:s}'"

    # Values
    max_eta = 2.6 if density == "high" else 1.85
    min_eta = 2.4 if density == "high" else 1.65

    energy = 100.
    epsilon = 0.01
    max_ene = energy + epsilon
    min_ene = energy - epsilon

    #  eta    ET     E
    # 1.75   5.0  14.8
    # 1.75  33.7 100.0
    # 1.75  40.0 118.6
    # 2.50   5.0  30.7
    # 2.50  16.3 100.0
    # 2.50  40.0 245.3
    energies = [31., 100., 245.] if density == "high" else [ 15., 100., 119.]

    process.generator.PGunParameters.ControlledByEta = cms.bool(True) # was False
    process.generator.PGunParameters.MaxEta = cms.double(max_eta) # was 2.7
    process.generator.PGunParameters.MinEta = cms.double(min_eta) # was 1.7
    #process.generator.PGunParameters.VarMax = cms.double(max_ene) # was 200.
    #process.generator.PGunParameters.VarMin = cms.double(min_ene) # was 25.
    process.generator.PGunParameters.VarValues = cms.vdouble(energies) # overrides VarMin/VarMax

    if verbose:
        print( "########################")
        print( "[customiseCloseBy]")
        print(f"density: '{density:s}'")
        print(f"MaxEta:   {max_eta:6.2f}")
        print(f"MinEta:   {min_eta:6.2f}")
        print(f"MaxVar:   {max_ene:6.2f}")
        print(f"MinVar:   {min_ene:6.2f}")
        print( "Energies:  ",", ".join([f"{x:.1f}" for x in energies]))
        print( "########################")

    return process
