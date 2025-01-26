from ps_simc_parser.parser import Parser

def main():
    parser = Parser()
    parser.spec = 'vengeance'  # Set spec before parsing
    
    # Parse the file
    with open('vdh.simc', 'r') as f:
        content = f.read()
    
    context = parser.parse_file_content(content)
    
    # Generate Lua code
    lua_code = parser.generate_lua(context)
    
    # Print parsed actions and Lua code
    print("Parsed Actions:")
    for action_list_name, actions in context.action_lists.items():
        print(f"\nAction List: {action_list_name}")
        for action in actions:
            print(f"  {action}")
    
    print("\nGenerated Lua Code:")
    print(lua_code)

if __name__ == '__main__':
    main() 