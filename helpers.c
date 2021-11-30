#include "helpers.h"
#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
  for (int i = 0; i < height; i++)
  {
      for (int  j = 0; j < width; j++)
      {
          int average = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0f);
          //hard code average
          image[i][j].rgbtBlue = average;
          image[i][j].rgbtGreen = average;
          image[i][j].rgbtRed = average;
      }
  }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{

    int widthInterval = floor(width / 2.0f);

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < widthInterval; j++)
        {
            //swap current cell with opposite cell; use a temp (leftmost with rightmost)
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][(width - 1) - j];
            image[i][(width - 1) - j] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //GET TEMP ARRAY!!! SWICTH VALUES LATER
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //iterate over 3*3 box; top to bottom left to right
            //manages vertical travel
            int averageBlue = 0;
            int averageGreen = 0;
            int averageRed = 0;
            
            float numbersInAvg = 0;

            for (int k = -1; k <= 1; k++)
            {

                for (int l = -1; l <= 1; l++)
                {
                    //if both i and j when modifed stay within bounds of picture
                    if ((i + k < height && i + k >= 0) && (j + l < width && j + l >= 0))
                    {
                        //printf("blue avg: %i, green avg: %i, red avg: %i\n",   image[i + k][j + l].rgbtBlue, image[i + k][j + l].rgbtGreen,  image[i + k][j + l].rgbtRed);
                        //add values for averaging
                        averageBlue += image[i + k][j + l].rgbtBlue;
                        averageGreen += image[i + k][j + l].rgbtGreen;
                        averageRed += image[i + k][j + l].rgbtRed;
                        //one more number is added to each average color
                        numbersInAvg++;
                    }
                }
            }
           
            //apply colour averages to our temp while code continues to excecute, this is so each pixel's values can stay consistent wile processing and thus so we can get accurate answers
            temp[i][j].rgbtBlue = round(averageBlue / numbersInAvg);
            temp[i][j].rgbtGreen = round(averageGreen / numbersInAvg);
            temp[i][j].rgbtRed = round(averageRed / numbersInAvg);
            
            //printf("blue avg: %i, green avg: %i, red avg: %i\n",  averageBlue, averageGreen,  averageRed);
        }
    }
    
    //apply new colors to image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
    

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
     //GET TEMP ARRAY!!! SWICTH VALUES LATER
    RGBTRIPLE temp[height][width];
    
    //make kernels!
    int Gx[3][3] = {
        {-1, 0, 1},
        {-2, 0, 2},
        {-1, 0, 1}
    };
    
    int Gy[3][3] = {
        {-1, -2, -1},
        {0, 0, 0},
        {1, 2, 1}
    };
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //gx and gy variables,
            float gxBlue = 0;
            float gyBlue = 0;
            
            float gxGreen = 0;
            float gyGreen = 0;
            
            float gxRed = 0;
            float gyRed = 0;
            
            
            for (int k = -1, gridNavY = 0; k <= 1; k++, gridNavY++)
            {

                for (int l = -1, gridNavX = 0; l <= 1; l++, gridNavX++)
                {
                    //if both i and j when modifed stay within bounds of picture
                    if ((i + k < height && i + k >= 0) && (j + l < width && j + l >= 0))
                    {
                        //mess with gx and gy values
                        gxBlue += image[i + k][j + l].rgbtBlue * Gx[gridNavY][gridNavX];
                        gyBlue += image[i + k][j + l].rgbtBlue * Gy[gridNavY][gridNavX];
                        
                        gxGreen += image[i + k][j + l].rgbtGreen * Gx[gridNavY][gridNavX];
                        gyGreen += image[i + k][j + l].rgbtGreen * Gy[gridNavY][gridNavX];
                        
                        gxRed += image[i + k][j + l].rgbtRed * Gx[gridNavY][gridNavX];
                        gyRed += image[i + k][j + l].rgbtRed * Gy[gridNavY][gridNavX];
                    }
                }    
            }
            //make calculations
            int NewBlue = round(sqrt(pow(gxBlue,2) + pow(gyBlue,2)));
            int NewGreen = round(sqrt(pow(gxGreen,2) + pow(gyGreen,2)));
            int NewRed = round(sqrt(pow(gxRed,2) + pow(gyRed,2)));
            
            //check if not  > 255 and apply to temp
            if (NewBlue > 255)
            {
                NewBlue = 255;
            }
            temp[i][j].rgbtBlue = NewBlue;
            
            if (NewGreen > 255)
            {
                NewGreen = 255;
            }
            temp[i][j].rgbtGreen = NewGreen;
            
            if (NewRed > 255)
            {
                NewRed = 255;
            }
            temp[i][j].rgbtRed = NewRed;
        }
    }
    
    
    //apply new colors to image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
    return;
}
