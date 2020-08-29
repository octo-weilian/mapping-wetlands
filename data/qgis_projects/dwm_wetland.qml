<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" hasScaleBasedVisibilityFlag="0" minScale="1e+08" version="3.4.12-Madeira" styleCategories="AllStyleCategories">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property key="WMSBackgroundLayer" value="false"/>
    <property key="WMSPublishDataSourceUrl" value="false"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="identify/format" value="Value"/>
  </customproperties>
  <pipe>
    <rasterrenderer band="1" type="paletted" opacity="1" alphaBand="-1">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <colorPalette>
        <paletteEntry alpha="0" color="#f7fbff" label="Non water" value="1"/>
        <paletteEntry alpha="255" color="#abdda4" label="Wetland" value="2"/>
        <paletteEntry alpha="255" color="#73b3d8" label="Seasonal water" value="3"/>
        <paletteEntry alpha="255" color="#08306b" label="Permanent water" value="4"/>
      </colorPalette>
      <colorramp name="[source]" type="gradient">
        <prop v="247,251,255,255" k="color1"/>
        <prop v="8,48,107,255" k="color2"/>
        <prop v="0" k="discrete"/>
        <prop v="gradient" k="rampType"/>
        <prop v="0.13;222,235,247,255:0.26;198,219,239,255:0.39;158,202,225,255:0.52;107,174,214,255:0.65;66,146,198,255:0.78;33,113,181,255:0.9;8,81,156,255" k="stops"/>
      </colorramp>
    </rasterrenderer>
    <brightnesscontrast contrast="0" brightness="0"/>
    <huesaturation colorizeRed="255" colorizeStrength="100" grayscaleMode="0" colorizeOn="0" colorizeBlue="128" colorizeGreen="128" saturation="0"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
