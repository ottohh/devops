using System;
using System.Diagnostics;
using System.IO;
using System.Text.Json;


var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();
builder.Services.AddHttpClient();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseHttpsRedirection();



app.MapGet("/status", async (IHttpClientFactory httpClientFactory) =>
{
        string logFile = "../data/vstorage"; // file to append to

        // Current timestamp
        string timestamp = DateTime.Now.ToString("yyyy-MM-ddTHH:mm:ssZ");

        // System uptime in hours (from Environment.TickCount64 in milliseconds)
        double uptimeHours = Environment.TickCount64 / 1000.0 / 3600.0;

        // Free disk space on root (C:) in MB
        var root = Path.GetPathRoot(Environment.SystemDirectory)??"/";
        DriveInfo drive = new DriveInfo(root);
        double freeDiskMB = drive.AvailableFreeSpace / (1024.0 * 1024.0);

        // Build log line
        string logLine = $"{timestamp} 2: uptime {uptimeHours:F2} hours, free disk in root: {freeDiskMB:F2} MBytes";

        // Append to file
        File.AppendAllText(logFile, logLine+ Environment.NewLine);

        var payload = new { log = logLine + Environment.NewLine };
        var json = JsonSerializer.Serialize(payload);

        var response = await httpClientFactory.CreateClient().PostAsync(
            "http://storage:8198/log",
            new StringContent(json, System.Text.Encoding.UTF8, "application/json")
        );

        
        return logLine;
});


app.Run();

