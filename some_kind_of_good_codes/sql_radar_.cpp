#include <iostream>

#include <sqltypes.h>
#include <sql.h>
#include <sqlext.h>

using namespace std;


void extract_error(
    string fn,
    SQLHANDLE handle,
    SQLSMALLINT type)
{
    SQLINTEGER   i = 0;
    SQLINTEGER   native;
    SQLCHAR      state[ 7 ];
    SQLCHAR      text[256];
    SQLSMALLINT  len;
    SQLRETURN    ret;

    cout << "\nThe driver reported the following diagnostics whilst running " << fn << "\n\n";

    do
    {
        ret = SQLGetDiagRec(type, handle, ++i, state, &native, text,
                            sizeof(text), &len );
        if (SQL_SUCCEEDED(ret))
            printf("%s:%ld:%ld:%s\n", state, i, native, text);
    }
    while( ret == SQL_SUCCESS );
}




int main() {
    // Veritabanı bağlantısı için gereken değişkenler
    SQLHANDLE henv;   // Environment Handle
    SQLHANDLE hdbc;   // Connection Handle
    SQLHANDLE hstmt;  // Statement Handle
    SQLRETURN retcode; // Return code

    // Environment handle oluşturma
    retcode = SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &henv);
    if (retcode != SQL_SUCCESS && retcode != SQL_SUCCESS_WITH_INFO) {
        cout << "Error creating Environment Handle!" << endl;
        return retcode;
    }

    // ODBC versionunu belirleme
    retcode = SQLSetEnvAttr(henv, SQL_ATTR_ODBC_VERSION, (void*)SQL_OV_ODBC3, 0);
    if (retcode != SQL_SUCCESS && retcode != SQL_SUCCESS_WITH_INFO) {
        cout << "Error setting Environment Attribute!" << endl;

        return retcode;
    }

    // Connection handle oluşturma
    retcode = SQLAllocHandle(SQL_HANDLE_DBC, henv, &hdbc);
    if (retcode != SQL_SUCCESS && retcode != SQL_SUCCESS_WITH_INFO) {
        cout << "Error creating Connection Handle!" << endl;
        return retcode;
    }

    // Veritabanına bağlanma
    SQLCHAR* connStr = (SQLCHAR*)"DRIVER={ODBC Driver 18 for SQL Server};SERVER=193.35.200.106;DATABASE=Prevla;UID=SA;PWD=hP337^9nArG&;TrustServerCertificate=Yes";
    retcode = SQLDriverConnect(hdbc, NULL, connStr, SQL_NTS, NULL, 0, NULL, SQL_DRIVER_NOPROMPT);
    if (retcode != SQL_SUCCESS && retcode != SQL_SUCCESS_WITH_INFO) {
        cout << "Error connecting to Database!" << endl;
        extract_error("SQLDriverConnect", hdbc, SQL_HANDLE_DBC);
        return retcode;
    }

    // Statement handle oluşturma
    retcode = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
    if (retcode != SQL_SUCCESS && retcode != SQL_SUCCESS_WITH_INFO) {
        cout << "Error creating Statement Handle!" << endl;
        return retcode;
    }

    // Sorgu çalıştırma
    retcode = SQLExecDirect(hstmt, (SQLCHAR*)"SELECT * FROM RadarDatas", SQL_NTS);
    if (retcode != SQL_SUCCESS && retcode != SQL_SUCCESS_WITH_INFO) {
        cout << "Error executing query!" << endl;
        return retcode;
    }

    //retcode = SQLExecDirect(hstmt, (SQLCHAR*)"INSERT INTO [dbo].[RadarDatas]([rdr_experiment_no],[rdr_frame_no],[rdr_total_points_in_frame],[rdr_point_no_in_frame],[rdr_y_radar],[rdr_x_radar],[rdr_z_radar],[rdr_vel_radar],[rdr_intensity_radar],[rdr_timestamp],[rdr_user],[rdr_date]) VALUES (1, 1, 1, 1 ,1.0 ,1.0 ,1.0 ,1.0 ,1.0 ,1.0 ,'burak' ,1.0)", SQL_NTS);

    // Sonuçları yazdırma
    SQLCHAR col1[256], col2[256];
    SQLLEN indicator1, indicator2;
    while (SQLFetch(hstmt) == SQL_SUCCESS) {
        SQLGetData(hstmt, 1, SQL_C_CHAR, col1, 256, &indicator1);
        SQLGetData(hstmt, 2, SQL_C_CHAR, col2, 256, &indicator2);
        cout << col1 << " " << col2 << endl;
    }

    // Handle'ların serbest bırakılması
   

    retcode = SQLExecDirect(hstmt, (SQLCHAR*)"INSERT INTO RadarDatas (rdr_experiment_no,rdr_frame_no,rdr_total_points_in_frame,rdr_point_no_in_frame,rdr_y_radar,rdr_x_radar,rdr_z_radar,rdr_vel_radar,rdr_intensity_radar,rdr_timestamp,rdr_user,rdr_date) VALUES (1, 1, 1, 1 ,1.0 ,1.0 ,1.0 ,1.0 ,1.0 ,1.0 ,'burak' ,1.0)", SQL_NTS);
    
    SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
    SQLDisconnect(hdbc);
    SQLFreeHandle(SQL_HANDLE_DBC, hdbc);
    SQLFreeHandle(SQL_HANDLE_ENV, henv);
    extract_error("SQLDriverConnect", hdbc, SQL_HANDLE_DBC);
return 0;
}