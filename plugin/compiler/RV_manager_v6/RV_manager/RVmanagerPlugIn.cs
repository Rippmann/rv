using System.IO;
using Rhino;
using System;

namespace RV_manager
{
    ///<summary>
    /// <para>Every RhinoCommon .rhp assembly must have one and only one PlugIn-derived
    /// class. DO NOT create instances of this class yourself. It is the
    /// responsibility of Rhino to create an instance of this class.</para>
    /// <para>To complete plug-in information, please also see all PlugInDescription
    /// attributes in AssemblyInfo.cs (you might need to click "Project" ->
    /// "Show All Files" to see it in the "Solution Explorer" window).</para>
    ///</summary>
    public class RVmanagerPlugIn : Rhino.PlugIns.PlugIn

    {
        public RVmanagerPlugIn()
        {
            Instance = this;
            RhinoApp.Idle += OnIdle; //subscribe
        }

        ///<summary>Gets the only instance of the RVmanagerPlugIn plug-in.</summary>
        public static RVmanagerPlugIn Instance
        {
            get; private set;
        }

        private void OnIdle(object sender, EventArgs e)
        {
            RhinoApp.Idle -= OnIdle; // unsubscribe

            string path = Rhino.PlugIns.PlugIn.PathFromName("rhinovault_V2");
            string plugin_dir = Path.GetDirectoryName(path);

            string command_dir = "commands";
            string command_path = Path.Combine(plugin_dir, command_dir);

            string[] files = System.IO.Directory.GetFiles(command_path, "*.py");

            //delete aliases
            //Rhino.ApplicationSettings.CommandAliasList.Delete(alias_del);

            foreach (string filepath in files)
            {
                //RhinoApp.WriteLine(filepath);
                string alias = Path.GetFileNameWithoutExtension(filepath);
                string macro = "_Noecho _-RunPythonScript " + filepath;

                Rhino.ApplicationSettings.CommandAliasList.Add(alias, macro);
            }

        }

        public override Rhino.PlugIns.PlugInLoadTime LoadTime
        {
            get { return Rhino.PlugIns.PlugInLoadTime.AtStartup; }
        }
    }
}

