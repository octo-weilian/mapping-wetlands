<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.4.12-Madeira" minScale="1e+08" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" maxScale="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property value="false" key="WMSBackgroundLayer"/>
    <property value="false" key="WMSPublishDataSourceUrl"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property value="Value" key="identify/format"/>
  </customproperties>
  <pipe>
    <rasterrenderer redBand="10" blueBand="1" alphaBand="-1" greenBand="8" opacity="1" type="multibandcolor">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>CumulativeCut</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <redContrastEnhancement>
        <minValue>46</minValue>
        <maxValue>2689</maxValue>
        <algorithm>StretchToMinimumMaximum</algorithm>
      </redContrastEnhancement>
      <greenContrastEnhancement>
        <minValue>200</minValue>
        <maxValue>4207</maxValue>
        <algorithm>StretchToMinimumMaximum</algorithm>
      </greenContrastEnhancement>
      <blueContrastEnhancement>
        <minValue>210</minValue>
        <maxValue>1086</maxValue>
        <algorithm>StretchToMinimumMaximum</algorithm>
      </blueContrastEnhancement>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0"/>
    <huesaturation grayscaleMode="0" saturation="0" colorizeGreen="128" colorizeBlue="128" colorizeStrength="100" colorizeOn="0" colorizeRed="255"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
