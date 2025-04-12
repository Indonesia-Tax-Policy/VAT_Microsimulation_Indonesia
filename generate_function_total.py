import pandas as pd

def generate_cal_vat_function():
    """
    Reads the Excel file at:
      C:/Users/adeda/microsimulation_manual/vat_microsim_Indo/susenas_2018_product_name_and_rate.xlsx
    and extracts the product names from the 'VATKODE' column.
    
    It then generates a Python function definition for cal_vat() whose parameters
    are the product names (cleaned to be valid Python identifiers) and whose body
    sums these parameters and returns the total.
    """
    # Path to the Excel file.
    file_path = r"C:/Users/adeda/Microsimulation/Tax_Microsimulation/indo_vat_category.xlsx"
    
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        raise Exception("Error reading the Excel file: " + str(e))
    
    if 'vat_cal' not in df.columns:
        raise ValueError("Column 'vat_cal' not found in the Excel file.")
    
    # Extract and clean the VATKODE values.
    vat_kodes = [str(item).strip() for item in df['vat_cal'].dropna().tolist()]
    # Replace spaces and dashes with underscores to ensure valid Python identifiers.
    valid_names = [name.replace(" ", "_").replace("-", "_") for name in vat_kodes]
    
    # Create the parameter list and the sum expression.
    params = ", ".join(valid_names)
    sum_expr = " + ".join(valid_names)
    
    # Generate the function definition as a string.
    func_lines = [
        "def cal_vat({}):".format(params),
        "    # Sum the VAT values for the following products:",
        "    # " + ", ".join(valid_names),
        "    total_vat = {}".format(sum_expr),
        "    return total_vat"
    ]
    
    function_def = "\n".join(func_lines)
    return function_def

if __name__ == '__main__':
    # Generate the function code.
    func_code = generate_cal_vat_function()
    
    # Save the generated function to a file.
    output_filename = "cal_vat_function.py"
    with open(output_filename, "w") as f:
        f.write("# This file was generated automatically.\n\n")
        f.write(func_code)
    
    print(f"Function saved in {output_filename}")
