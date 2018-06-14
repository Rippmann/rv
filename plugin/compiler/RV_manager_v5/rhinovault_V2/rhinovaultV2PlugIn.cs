using System.IO;
using Rhino;
using System;

namespace rhinovault_V2
{
    ///<summary>
    /// <para>Every RhinoCommon .rhp assembly must have one and only one PlugIn-derived
    /// class. DO NOT create instances of this class yourself. It is the
    /// responsibility of Rhino to create an instance of this class.</para>
    /// <para>To complete plug-in information, please also see all PlugInDescription
    /// attributes in AssemblyInfo.cs (you might need to click "Project" ->
    /// "Show All Files" to see it in the "Solution Explorer" window).</para>
    ///</summary>
    public class rhinovaultV2PlugIn : Rhino.PlugIns.PlugIn

    {
        public rhinovaultV2PlugIn()
        {
            Instance = this;
            RhinoApp.Idle += OnIdle; //subscribe

        }

        ///<summary>Gets the only instance of the rhinovaultV2PlugIn plug-in.</summary>
        public static rhinovaultV2PlugIn Instance
        {
            get; private set;
        }

        private void OnIdle(object sender, EventArgs e)
        {
            RhinoApp.Idle -= OnIdle; // unsubscribe

            string path = Rhino.PlugIns.PlugIn.PathFromName("rhinovault_V2");
            string plugin_dir = Path.GetDirectoryName(path);

            string command_dir_1 = "compas_rv";
            string command_dir_2 = "commands";
            string command_path = Path.Combine(plugin_dir, command_dir_1);
            command_path = Path.Combine(command_path, command_dir_2);

            string[] files = System.IO.Directory.GetFiles(command_path, "*.py");

            //delete aliases
            //Rhino.ApplicationSettings.CommandAliasList.Delete(alias_del);

            foreach (string filepath in files)
            {

                bool b = filepath.Contains("RV");
                if (b)
                {
                    //RhinoApp.WriteLine(filepath);
                    string alias = Path.GetFileNameWithoutExtension(filepath);
                    string macro = "_Noecho _-RunPythonScript " + filepath;

                    Rhino.ApplicationSettings.CommandAliasList.Add(alias, macro);
                }
            }

            //RhinoApp.RunScript("_-Line 0,0,0 10,10,10", false);

            //_Noecho 

            string scr_dir = plugin_dir.Replace(@"\",@"\\");


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
            //RhinoApp.WriteLine(cmd);

            //"sys.path.append(path)" +
            //Environment.NewLine +
            //"print sys.path" +
            //Environment.NewLine +

            RhinoApp.RunScript(cmd, false);
           

        }

        public override Rhino.PlugIns.PlugInLoadTime LoadTime
        {
            get { return Rhino.PlugIns.PlugInLoadTime.AtStartup;}
        }

    }
}