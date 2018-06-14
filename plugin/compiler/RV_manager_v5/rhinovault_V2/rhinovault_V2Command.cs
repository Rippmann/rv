using System;
using System.IO;
using System.Collections.Generic;
using Rhino;
using Rhino.Commands;
using Rhino.Geometry;
using Rhino.Input;
using Rhino.Input.Custom;

namespace rhinovault_V2
{
    [
        System.Runtime.InteropServices.Guid("6777ddc6-cc06-4a98-93b9-1950a43bbe9c")
    ]
    //,Rhino.Commands.CommandStyle(Rhino.Commands.Style.ScriptRunner)
    public class rhinovault_V2Command : Command
    {
        public rhinovault_V2Command()
        {
            // Rhino only creates one instance of each command class defined in a
            // plug-in, so it is safe to store a refence in a static property.
            Instance = this;
        }

        ///<summary>The only instance of this command.</summary>
        public static rhinovault_V2Command Instance
        {
            get; private set;
        }

        ///<returns>The command name as it appears on the Rhino command line.</returns>
        public override string EnglishName
        {
            get { return "RVinit"; }
        }

        protected override Result RunCommand(RhinoDoc doc, RunMode mode)
        {
            // TODO: start here modifying the behaviour of your command.
            // ---
            RhinoApp.WriteLine("dssd");
            string path = Rhino.PlugIns.PlugIn.PathFromName("rhinovault_V2");
            string plugin_dir = Path.GetDirectoryName(path);

            string scr_dir = plugin_dir.Replace(@"\", @"\\");


            string cmd = "_Noecho -_RunPythonScript (" +
                            Environment.NewLine +
                            "import sys" +
                            Environment.NewLine +
                            "import scriptcontext as sc" +
                            Environment.NewLine +
                            "path = " + "'" + scr_dir + "'" +
                            Environment.NewLine +
                            "sc.sticky['path'] = path" +
                            Environment.NewLine +
                            ")";
            RhinoApp.WriteLine(cmd);
            RhinoApp.RunScript(cmd, false);




            return Result.Success;
        }
    }
}
