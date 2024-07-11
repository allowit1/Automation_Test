using System;
using System.Collections.Generic;
using System.IO;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

class Program
{
    static void Main(string[] args)
    {
        // Example usage:
        string filePath = @"C:\Users\User\Documents\Automation_Test\AutomationTest\groups\TestOfAutomation.yml";

        // Create directory if it doesn't exist
        string directoryPath = Path.GetDirectoryName(filePath);
        if (!Directory.Exists(directoryPath))
        {
            Directory.CreateDirectory(directoryPath);
        }

        // Check if file exists, if not create an empty YAML file
        if (!File.Exists(filePath))
        {
            File.WriteAllText(filePath, "example_group1: []");
        }

        // Add a partner
        AddPartner(filePath, "example_group1", "new_partner");

         // Add a partner
        AddPartner(filePath, "example_group1", "new_partner2");

        // Remove a partner
        RemovePartner(filePath, "example_group1", "new_partner");
    }

    static Dictionary<string, object> ReadYaml(string filePath)
    {
        try
        {
            var deserializer = new DeserializerBuilder()
                .WithNamingConvention(CamelCaseNamingConvention.Instance)
                .Build();

            using (var reader = new StreamReader(filePath))
            {
                var yamlObject = deserializer.Deserialize<Dictionary<string, object>>(reader);
                return yamlObject;
            }
        }
        catch (FileNotFoundException)
        {
            Console.WriteLine($"File not found: {filePath}");
            Environment.Exit(1);
        }
        catch (YamlDotNet.Core.YamlException e)
        {
            Console.WriteLine($"YAML syntax error in file {filePath}: {e.Message}");
            Environment.Exit(1);
        }
        return null; // This line will never be reached because Environment.Exit will terminate the application.
    }

    static void WriteYaml(string filePath, Dictionary<string, object> data)
    {
        try
        {
            var serializer = new SerializerBuilder()
                .WithNamingConvention(CamelCaseNamingConvention.Instance)
                .Build();

            using (var writer = new StreamWriter(filePath))
            {
                serializer.Serialize(writer, data);
            }
        }
        catch (UnauthorizedAccessException)
        {
            Console.WriteLine($"Permission denied: {filePath}");
            Environment.Exit(1);
        }
        catch (Exception e)
        {
            Console.WriteLine($"An error occurred while writing to the file: {e.Message}");
            Environment.Exit(1);
        }
    }

    static void AddPartner(string filePath, string group, string partner)
    {
        var data = ReadYaml(filePath);

        if (data.ContainsKey(group))
        {
            var partners = (List<object>)data[group];
            if (!partners.Contains(partner))
            {
                partners.Add(partner);
            }
        }
        else
        {
            data[group] = new List<object> { partner };
        }

        WriteYaml(filePath, data);
        Console.WriteLine($"Partner {partner} added to {group}");
    }

    static void RemovePartner(string filePath, string group, string partner)
    {
        var data = ReadYaml(filePath);

        if (data.ContainsKey(group))
        {
            var partners = (List<object>)data[group];
            if (partners.Contains(partner))
            {
                partners.Remove(partner);
            }
        }

        WriteYaml(filePath, data);
        Console.WriteLine($"Partner {partner} removed from {group}");
    }
}
