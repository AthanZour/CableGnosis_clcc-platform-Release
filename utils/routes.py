"""
Flask routes for external popup windows used in Monitoring tab.
---------------------------------------------------------------
- /toolbox        : Auxiliary window triggered by 'Open Toolbox'
- /import         : Data import options (triggered by 'Import Data')
- /coordinates    : PMU coordinate format & map options
"""

from flask import Flask

def register_routes(server: Flask):
    @server.route("/toolbox")
    def toolbox_page():
        """Popup window for the Toolbox."""
        return """
        <html>
        <head><title>Toolbox</title></head>
        <body style='font-family:Arial; padding:16px; background:#fafafa;'>
          <h2 style='color:#333'>🔧 Auxiliary Toolbox</h2>
          <p>This popup was opened from the <b>Monitoring</b> tab.</p>
          <hr>
          <ul>
            <li>Perform quick checks</li>
            <li>View diagnostic KPIs</li>
            <li>Access microservice stats</li>
          </ul>
          <p style='margin-top:20px;color:#666'><i>Close this window when done.</i></p>
        </body></html>
        """

    # ---------------------------------------------------------------------
    @server.route("/import")
    def import_popup():
        """Popup window for importing datasets."""
        return """
        <html>
        <head><title>Import Data</title></head>
        <body style='font-family:Arial; padding:16px; background:#f9f9f9;'>
          <h2 style='color:#333'>📁 Import Data</h2>
          <p>Select dataset type and import mode:</p>
          <form style='margin-top:10px;'>
            <label>Dataset type:</label><br>
            <input type='radio' name='dtype' checked> Real Data<br>
            <input type='radio' name='dtype'> Test / Synthetic<br><br>

            <label>PMU Target:</label><br>
            <select>
              <option>PMU #1</option>
              <option>PMU #2</option>
            </select><br><br>

            <label>Upload file:</label><br>
            <input type='file' accept='.csv,.json'><br><br>

            <input type='checkbox' checked> Temporary test mode<br>
            <input type='checkbox'> Save configuration<br><br>

            <button style='padding:6px 12px;'>Import</button>
          </form>
          <p style='margin-top:20px;color:#666'><i>This window simulates the Import Data popup.</i></p>
        </body></html>
        """

    # ---------------------------------------------------------------------
    @server.route("/coordinates")
    def coord_popup():
        """Popup window for coordinate display options."""
        return """
        <html>
        <head><title>Coordinate Options</title></head>
        <body style='font-family:Arial; padding:16px; background:#fdfdfd;'>
          <h2 style='color:#333'>📍 Coordinate Options</h2>
          <p>Choose coordinate display format:</p>
          <ul>
            <li>Degrees (Lat/Lon)</li>
            <li>Absolute (X/Y)</li>
            <li>Radians (alternative)</li>
          </ul>
          <hr>
          <p>
            <b>View location:</b><br>
            <a href='https://www.google.com/maps?q=34.700123,33.312345'
               target='_blank' style='color:#0077cc; text-decoration:none;'>
               Open current PMU position in Google Maps
            </a>
          </p>
          <p style='margin-top:20px;color:#666'><i>Mini options panel for coordinate display.</i></p>
        </body></html>
        """

    # ---------------------------------------------------------------------
    # Optional: a simple health-check or about route
    @server.route("/about")
    def about_page():
        return """
        <html>
        <head><title>About</title></head>
        <body style='font-family:Arial;padding:16px;'>
          <h3>About UCY Monitoring Platform</h3>
          <p>Demo environment for data visualization, PMU monitoring and synthetic generation.</p>
          <p>Version: 3.0</p>
        </body></html>
        """
