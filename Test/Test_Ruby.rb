require 'yaml'

# Method to read YAML file
def read_yaml(file_path)
  begin
    YAML.load_file(file_path)
  rescue Errno::ENOENT
    puts "File not found: #{file_path}"
    exit
  rescue Psych::SyntaxError => e
    puts "YAML syntax error in file #{file_path}: #{e.message}"
    exit
  end
end

# Method to write YAML file
def write_yaml(file_path, data)
  begin
    File.open(file_path, 'w') do |file|
      file.write(data.to_yaml)
    end
  rescue Errno::EACCES
    puts "Permission denied: #{file_path}"
    exit
  rescue => e
    puts "An error occurred while writing to the file: #{e.message}"
    exit
  end
end

# File path
file_path = 'example.yaml'

# Read the existing YAML file
data = read_yaml(file_path)

# New data to add
new_entries = ["itamar0000"]

# Check if the key exists and merge new data
if data['example_group1']
  data['example_group1'] += new_entries
else
  data['example_group1'] = new_entries
end

# Write the updated data back to the YAML file
write_yaml(file_path, data)

puts "Data successfully added to #{file_path}"
